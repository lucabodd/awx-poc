# This is just for the debugging phases...
set -x
set -e

# Root user detection
if [ $(echo "$UID") = "0" ]; then
    sudo_cmd=''
else
    sudo_cmd='sudo'
fi

isUUID() {
    if [[ "$1" =~ ^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$ ]]; then
        return 0
    else
        return 1
    fi
}

CONTROL_NODE_ID=bd17d637-3499-49c8-a4c5-e6ca5b9ad205
API_KEY=${API_KEY:-$CONTROL_NODE_ID}
HOST_ID=$(curl -k -k --silent 'https://api.agent.alienvault.cloud/osquery-api/eu-central-1/bootstrap?flavor=deb' | grep HOST_ID= |grep 000 | awk -F= '{print $2}')
BASE=/etc/osquery
SECRETFILE="${BASE}/secret"
ASSUME_YES=true

if [ -n "$API_KEY" ] && ! isUUID $API_KEY; then
    echo "Error: CONTROL_NODE_ID is not valid"
    exit 1
fi

if [ -n "$HOST_ID" ] && ! isUUID $HOST_ID; then
    echo "Error: ASSET_ID is not valid"
    exit 1
fi

if [ -z "$API_KEY" ]; then
    if [ -f "$SECRETFILE" ]; then
        API_KEY=$($sudo_cmd cat "${SECRETFILE}")
        echo "Detected secret file, verifying value"
        if ! isUUID "$API_KEY"; then
            echo "Error: Value in \"${SECRETFILE}\" is corrupted."
            echo "This could be due to an error during a previous installation. To fix, delete the secret file and re-run the Bootstrap Installation command"
            echo "Contact AT&T CyberSecurity Support for more information."
            exit 1
        fi
    fi
fi

if [ -z "$API_KEY" ]; then
    echo "Error: You must supply either the API_KEY or CONTROL_NODE_ID environment variable to identify your agent account"
    exit 1
fi
echo "Checking if osquery is installed..."
errcode=0
$sudo_cmd dpkg-query -W osquery || { errcode=1; }

ASSUME_YES=${ASSUME_YES:-false}
if [ $errcode -eq 0 ]; then
    if ! $ASSUME_YES; then
        echo " *** ACHTUNG! *** "
        echo " AlienVault Agent cannot be installed along with Osquery. "
        echo " This script will now attempt to delete Osquery and its configuration files "
        echo " (Set environment variable ASSUME_YES=true in the future to automatically uninstall osquery if found)"
        read -p " Continue? [Y/N] " -n 1 -r

        if [[ $REPLY =~ ^[Nn]$ ]]
        then
            exit 1 # Just exit with error code.
        fi
    fi

    $sudo_cmd apt-get purge osquery --assume-yes

    # Clean remaining directories, for sanity.
    $sudo_cmd rm -rf /var/osquery /var/log/osquery
fi

if [ -z "$HOST_ID" ]; then
    # Debian package manager APT will restore osquery.flags.default to osquery.flags
    # as a part of install, so verify Host ID in file to avoid broken install
    FLAGFILE_DEFAULT="${BASE}/osquery.flags.default"

    if [ -f "$FLAGFILE_DEFAULT" ]; then
        HOST_ID=$(grep specified_identifier "$FLAGFILE_DEFAULT" | sed s/--specified_identifier=//)

        if [ -n "$HOST_ID" ]; then
            echo "Detected osquery.flags file, verifying value"
            if ! isUUID "$HOST_ID"; then
                echo "Error: Value in \"${FLAGFILE_DEFAULT}\" is corrupted."
                echo "This could be due to an error during a previous installation. To fix, delete the osquery.flags.default file and re-run the Bootstrap Installation command"
                echo "Contact AT&T CyberSecurity Support for more information."
                exit 1
            else
                echo "Re-using previously selected host id from ${FLAGFILE_DEFAULT}: ${HOST_ID}"
            fi
        fi
    fi
fi

echo "Downloading and installing image"
errcode=0
$sudo_cmd dpkg-query -W apt-transport-https || { errcode=1; } 
$sudo_cmd dpkg-query -W curl || { errcode=1; }
$sudo_cmd dpkg-query -W gnupg || { errcode=1; }

if [ $errcode -ne 0 ]; then
        $sudo_cmd apt-get install -y apt-transport-https curl gnupg
fi

curl -k -s https://agent-packageserver.alienvault.cloud/repo/deb/pool/stable/a/al/alienvault-agent_20.08.0003.0301_amd64.deb --output alienvault-agent.deb
$sudo_cmd dpkg -i alienvault-agent.deb
echo "Writing secret"
$sudo_cmd bash -c "echo ${API_KEY} > ${SECRETFILE}"
$sudo_cmd chmod go-rwx "$SECRETFILE"

echo "Setting up flag file"
FLAGFILE="${BASE}/osquery.flags"

if [ -z "$HOST_ID" ]; then
    if [ -f "$FLAGFILE" ]; then
        HOST_ID=$(grep specified_identifier "$FLAGFILE" | sed s/--specified_identifier=//)
    fi

    if [ -z "$HOST_ID" ]; then
        HOST_ID=00000000-9ef4-4723-904d-6b02d65e18dc
    else
        echo "Detected osquery.flags file, verifying value"
        if ! isUUID $HOST_ID; then
            echo "Error: Value in \"${FLAGFILE}\" is corrupted."
            echo "This could be due to an error during a previous installation. To fix, delete the osquery.flags and osquery.flags.default file and re-run the Bootstrap Installation command"
            echo "Contact AT&T CyberSecurity Support for more information."
            exit 1
        fi
        echo "Re-using previously selected host id from ${FLAGFILE}: ${HOST_ID}"
    fi
fi

$sudo_cmd cp "${BASE}/osquery.flags.example" "${FLAGFILE}"

echo "Setting host identifier"
$sudo_cmd bash -c "echo --tls_hostname=api.agent.alienvault.cloud/osquery-api/eu-central-1 >> ${FLAGFILE}"
$sudo_cmd bash -c "echo --host_identifier=specified >> ${FLAGFILE}"
$sudo_cmd bash -c "echo --specified_identifier=${HOST_ID} >> ${FLAGFILE}"
$sudo_cmd bash -c "echo --watchdog_memory_limit=350 >> ${FLAGFILE}"
$sudo_cmd bash -c "echo --watchdog_utilization_limit=110 >> ${FLAGFILE}"

echo "Restarting osqueryd"
$sudo_cmd service osqueryd restart
