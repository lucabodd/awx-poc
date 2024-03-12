# This is just for the debugging phases...
set -x
set -e
CONTROL_NODE_ID=bd17d637-3499-49c8-a4c5-e6ca5b9ad205
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

API_KEY=${API_KEY:-$CONTROL_NODE_ID}
HOST_ID=$(curl -k --silent 'https://api.agent.alienvault.cloud/osquery-api/eu-central-1/bootstrap?flavor=rpm' | grep HOST_ID= |grep 000 | awk -F= '{print $2}')
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
if ! $sudo_cmd yum list installed yum-utils > /dev/null 2>&1; then
    echo "Installing yum-utils..."
    $sudo_cmd yum install -y yum-utils > /dev/null 2>&1
fi

echo "Downloading and installing image"
curl -k -L https://agent-packageserver.alienvault.cloud/repo/GPG.key > /etc/pki/rpm-gpg/RPM-GPG-KEY-alienvault-agent
$sudo_cmd /bin/bash -c "cat > /tmp/alienvault-agent.repo" <<'EOF'
[alienvault-agent-rpm]
name=name=AlienVault Agent RPM Repo - $basearch
baseurl=https://agent-packageserver.alienvault.cloud/repo/rpm/$basearch/
enabled=1
sslverify=0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-alienvault-agent
gpgcheck=1
EOF
$sudo_cmd yum-config-manager --add-repo /tmp/alienvault-agent.repo
$sudo_cmd rm /tmp/alienvault-agent.repo
$sudo_cmd yum-config-manager --enable alienvault-agent-rpm
$sudo_cmd yum install -y alienvault-agent-20.08.0003.0301
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
        HOST_ID=00000000-4473-4181-8d51-1b72fec95ec6
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
