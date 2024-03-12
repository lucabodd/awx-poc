import datetime
import json
import re
from jira import JIRA
import requests
from htmlMailGenerator import * 


user='{{ username }}'
user_mail=user+'@kaleyra.com'
kaleyra_sec_team=['luca.bodini@kaleyra.com', 'federico.donati@kaleyra.com']
alienvault_endpoint='https://kaleyrainc.alienvault.cloud'
alienvault_password='{{ alienvault_password }}'


# init alienvault session:
r = requests.get(alienvault_endpoint+"/api/2.0/uiconfig")
preauth_x_xsrf_token = r.cookies['XSRF-TOKEN']
preauth_session_cookies = r.cookies
alienvault_login_creds = { 'email': user_mail, 'password': alienvault_password }
r = requests.post(alienvault_endpoint+'/api/2.0/login', cookies=preauth_session_cookies, json=alienvault_login_creds, headers = {'X-Xsrf-Token': preauth_x_xsrf_token} )
session_cookies = r.cookies
r = requests.get(alienvault_endpoint+'/api/2.0/users/me', cookies=session_cookies, headers = {'X-Xsrf-Token': preauth_x_xsrf_token})
x_xsrf_token = r.cookies['XSRF-TOKEN']

# list to exclude hosts from meing deleted
exclude_from_match = ['eks']

print_head()
print_header()
print_title("AlienVault Inventory - Remove Duplicated Assets")
print_subtitle("Routine executed {{ ansible_date_time.date }} {{ ansible_date_time.hour }}:{{ ansible_date_time.minute }}:{{ ansible_date_time.second }}")
print_item_section("Discovered Duplicated Assets:")

r = requests.get(alienvault_endpoint+'/api/2.0/assets/search/r?size=10000&page=0&query=knownAsset==%27true%27&sort=updated,desc', cookies=session_cookies, headers = {'X-Xsrf-Token': x_xsrf_token} )
all_assets=json.loads(r.text)

mod_count=0
warnings_count=0
all_assets_names = []

for asset in all_assets['_embedded']['assets']:
    all_assets_names.append(asset['name'])

seen = set()
seen_add = seen.add
assets_seen_twice = set( x for x in all_assets_names if x in seen or seen_add(x) )

for duplicated_asset in assets_seen_twice:
    r = requests.get(alienvault_endpoint+'/api/2.0/assets/search/r?size=20&page=0&query=knownAsset==%27true%27;name==%27'+duplicated_asset+'%27&sort=updated,desc', cookies=session_cookies, headers = {'X-Xsrf-Token': x_xsrf_token} )
    duplicated_entries=json.loads(r.text)
    last_updated = duplicated_entries['_embedded']['assets'][0]['created']
    
    if not any(substring in duplicated_entries['_embedded']['assets'][0]['name'] for substring in exclude_from_match):
        if len(duplicated_entries['_embedded']['assets']) > 1:
            print_item_description("Found Duplicates For {}".format(duplicated_entries['_embedded']['assets'][0]['name']))
        for i in range(1, len(duplicated_entries['_embedded']['assets'])):
            asset=duplicated_entries['_embedded']['assets'][i]
            print_item("Deleting "+asset['name']+" ID: "+asset['id'])
            r = requests.delete(alienvault_endpoint+'/api/2.0/assets/'+asset['id'], cookies=session_cookies, headers = {'X-Xsrf-Token': x_xsrf_token})
            if(r.status_code==200):
                mod_count = mod_count+1
            else:
                warnings_count = warnings_count+1
        print_item_list_end()

print_item_footer()
print_spacer()
print_counter_two(mod_count, "Removed Duplicated Hosts", warnings_count, "Warnings")
print_footer()

if(mod_count>0 or warnings_count>0):
    print("send_mail_true")

