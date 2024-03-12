import requests
import json
from jira import JIRA
#from htmlMailGenerator import *

#auth section
jira_endpoint='https://kaleyra.atlassian.net'
user='luca.bodini'
user_mail=user+'@kaleyra.com'
jira_user_api_token=''
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))

headers = {
    "accept": "application/json",
    "X-ApiKeys": "accessKey=;secretKey="
}


#Main
asset_id="0a862eda-e058-44a0-be88-b2da0832e6fe"
plugin_id="168428"

url = "https://cloud.tenable.com/workbenches/assets/"+asset_id+"/vulnerabilities/"+plugin_id+"/info"



response = requests.get(url, headers=headers)
vulnerability_details = json.loads(response.text)

url = "https://cloud.tenable.com/assets/"+asset_id

response = requests.get(url, headers=headers)
asset_details = json.loads(response.text)

asset_details_pretty = json.dumps(asset_details, indent=2)
vulnerability_details_pretty = json.dumps(vulnerability_details, indent=2)
print(asset_details_pretty)
print(vulnerability_details_pretty)

separator=" "
cvss3=float(vulnerability_details['info']['risk_information']['cvss3_base_score'])
tenable_asset_id=asset_details['id']
tenable_has_agent=asset_details['has_agent']
tenable_last_authenticated_scan_date=asset_details['last_authenticated_scan_date']
hostname = separator.join(asset_details['hostname']) 
agent_name=separator.join(asset_details['agent_name'])
fqdn=separator.join(asset_details['fqdn'])
operating_system=separator.join(asset_details['operating_system'])
aws_ec2_instance_id=separator.join(asset_details['aws_ec2_instance_id']) if len(asset_details['aws_ec2_instance_id'])>0 else ""
aws_owner_id=separator.join(asset_details['aws_owner_id']) if len(asset_details['aws_owner_id'])>0 else ""
aws_region=separator.join(asset_details['aws_region']) if len(asset_details['aws_region'])>0 else ""
aws_vpc_id=separator.join(asset_details['aws_vpc_id']) if len(asset_details['aws_vpc_id'])>0 else ""
aws_ec2_instance_group_name=separator.join(asset_details['aws_ec2_instance_group_name']) if len(asset_details['aws_ec2_instance_group_name'])>0 else "" 

details=""
details=details + "*Hostname:* "+hostname+"\n"
details=details + "*Agent Name:* "+agent_name+"\n"
details=details + "FQDN: "+fqdn+"\n"
details=details + "Operating System: "+operating_system+"\n"
details=details + "AWS Instance ID: "+aws_ec2_instance_id+"\n" if aws_ec2_instance_id!="" else ""
details=details + "AWS Owner ID: "+aws_owner_id+"\n" if aws_owner_id!="" else ""
details=details + "AWS Region: "+aws_region+"\n" if aws_region!="" else ""
details=details + "AWS VPC ID: "+aws_vpc_id+"\n" if aws_vpc_id!="" else ""
details=details + "AWS VPC ID: "+aws_ec2_instance_group_name+"\n" if aws_ec2_instance_group_name!="" else ""
details=details + "Tenable Asset ID: "+tenable_asset_id+"\n"
details=details + "Has Agent: "+str(tenable_has_agent)+"\n"
details=details + "Last Authenticated Scan: "+tenable_last_authenticated_scan_date+"\n"

if (cvss3 < 1):
    severity = "Informational Only"
if (cvss3 >= 1.0 or cvss3 >=3.9):
    severity = "Low"
if (cvss3 >= 4.0 or cvss3<=6.9):
    severity = "Medium"
if (cvss3 >= 7.0 or cvss3 <=8.9 ):
    severity = "High"
if (cvss3 >= 9.0):
    severity = "Critical"

description ="*Description:* \n"+vulnerability_details['info']['description']+"\n ---- \n *Synopsys:* \n"+vulnerability_details['info']['synopsis']+" \n ---- \n *Recommendations:* \n"+vulnerability_details['info']['solution']+" \n ---- \n *Severity:* "+severity+"\n ---- \n *Endpoint(s) and plugin Details:*\n"+details


issue_dict = {
    'project': 'COR',
    'summary': vulnerability_details['info']['plugin_details']['name'],
    'description': description,
    'issuetype': {'name': 'COR - Task'},
    'customfield_10683': { 'value' : severity},
    'parent': {'key': 'COR-3707'},
}

 
new_issue = auth_jira.create_issue(fields=issue_dict)


print(severity)