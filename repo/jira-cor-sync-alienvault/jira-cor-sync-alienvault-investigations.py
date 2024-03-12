import datetime
import json
import re
from jira import JIRA
import requests
from htmlMailGenerator import *
import logging
from datetime import date
import markdownify

version="2.0.7"

user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
jira_executor_account_id='{{ jira_executor_account_id }}' # Luca Bodini : 5f7d69a13fe07600699920b8
                                                    # Federico Donati : 5d6e0cc74b5fce0db430cd77
kaleyra_sec_team=['luca.bodini@kaleyra.com', 'federico.donati@kaleyra.com']
alienvault_endpoint='https://kaleyrainc.alienvault.cloud'
alienvault_investigations_endpoint='https://investigations.eu-central-1.prod.alienvault.cloud'
alienvault_password='{{ alienvault_password }}'
jira_endpoint='https://kaleyra.atlassian.net'
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))

# init alienvault session (old):
#r = requests.get(alienvault_endpoint+"/api/2.0/uiconfig")
#preauth_x_xsrf_token = r.cookies['XSRF-TOKEN']
#preauth_session_cookies = r.cookies
#alienvault_login_creds = { 'email': user_mail, 'password': alienvault_password }
#r = requests.post(alienvault_endpoint+'/api/2.0/login', cookies=preauth_session_cookies, json=alienvault_login_creds, headers = {'X-Xsrf-Token': preauth_x_xsrf_token} )
#session_cookies = r.cookies
#r = requests.get(alienvault_endpoint+'/api/2.0/users/me', x_, headers = {'X-Xsrf-Token': preauth_x_xsrf_token})
#x_xsrf_token = r.cookies['XSRF-TOKEN']

## Init alienvault session API token
r = requests.post('https://kaleyrainc.alienvault.cloud/api/2.0/oauth/token',
    params={ 'grant_type': 'client_credentials',},
    headers={ 'Content-Type': 'application/x-www-form-urlencoded',},
    auth=('awx-client-donati', alienvault_password),
)
auth_payload=json.loads(r.text)
headers = {"Authorization": "Bearer "+auth_payload['access_token'] }

# Init log module
# set up logging to file - see previous section for more details
# Logging Rules:
# Debug: All updates on issues
# Info: Starting/ending/ procedure
# Warning: recoverable error that does not require the user's interaction for recovery
# error: recoverable error that requires the user's interaction for recovery
# critical: unrecoverable error that quits the execution 
today = date.today()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/awx-cor-sync-alienvault-investigations-'+str(today)+'.log')

print_head()
print_header()
print_title("COR - Alienvault Sync Investigations")
print_subtitle("Schedule executed 2023-08-30 09:30:24")
logging.info("COR AlienVault sync investigations "+version+" starting procedure at: 2023-08-30 09:30:24")

######################################################
# Create jira ticket when new investigation is found #
######################################################
print_item_section("Creating Jiras For New AlienVault Investigations")
logging.info("Creating Jiras For New AlienVault Investigations")
new_tickets_mod_count = 0

json_data = {
    'q': "deployment=='kaleyrainc';status=='Open'",
}
r = requests.post(alienvault_investigations_endpoint+'/investigations/v3/investigations/search', headers=headers, json=json_data)
open_investigations=json.loads(r.text)

if not('investigations' in open_investigations):
    if r.status_code==401:
        print_item_description("Error 401 (Unauthorized): Invalid session cookie - Full authentication is required to access this resource")
        logging.critical("Error 401 (Unauthorized): Invalid session cookie. Full authentication is required to access this resource")
        print("send_mail_true")
        quit()
    print_item_footer()
    print_spacer()

if open_investigations['page']['totalElements'] > 0:
    for investigation in open_investigations['investigations']:
        print_item_description("Found <a href='{}/#/investigations/eu-central-1/{}'>new open investigation {}</a>".format(alienvault_endpoint, investigation['id'], investigation['id']))
        logging.debug("Found {}/#/investigations/eu-central-1/{}' new open investigation {}".format(alienvault_endpoint, investigation['id'], investigation['id']))
        print_item(investigation['title'])
        r = requests.get(investigation['_links']['notes']['href'], headers=headers)
        investigation_notes=json.loads(r.text)

        
        # in this section adding text formatting to make the text more appealing
        # RULES mast be put in order from the more specific match to the least specific
        formatted_investigation_notes = investigation_notes['notes'][len(investigation_notes['notes'])-1]['message']
        """
        #Generic
        formatted_investigation_notes = formatted_investigation_notes.replace("\/", "/")
        formatted_investigation_notes = formatted_investigation_notes.replace(",", ", ")
        formatted_investigation_notes = formatted_investigation_notes.replace("--A", "A")
        formatted_investigation_notes = formatted_investigation_notes.replace("--R", "R")
        formatted_investigation_notes = formatted_investigation_notes.replace("--S", "S")
        # Analysis
        formatted_investigation_notes = formatted_investigation_notes.replace("**ANALYSIS**", "ANALYSIS")
        formatted_investigation_notes = formatted_investigation_notes.replace("ANALYSIS", "----\n*ANALYSIS*")
        formatted_investigation_notes = formatted_investigation_notes.replace("Analysis", "----\n*ANALYSIS*")
        # Recommendation
        formatted_investigation_notes = formatted_investigation_notes.replace("**RECOMMENDATION**", "RECOMMENDATION")
        formatted_investigation_notes = formatted_investigation_notes.replace("RECOMMENDATIONS", "RECOMMENDATION")
        formatted_investigation_notes = formatted_investigation_notes.replace("Recommendation", "RECOMMENDATION")
        formatted_investigation_notes = formatted_investigation_notes.replace("RECOMMENDATION", "----\n*RECOMMENDATION*")

        # Artifacts
        formatted_investigation_notes = formatted_investigation_notes.replace("ARTIFACTS//FINDINGS", "ARTIFACTS")
        formatted_investigation_notes = formatted_investigation_notes.replace("FINDINGS/ARTIFACTS", "ARTIFACTS")
        formatted_investigation_notes = formatted_investigation_notes.replace("**ARTIFACTS & FINDINGS**", "ARTIFACTS")
        formatted_investigation_notes = formatted_investigation_notes.replace("Artifacts", "ARTIFACTS")
        formatted_investigation_notes = formatted_investigation_notes.replace("ARTIFACTS", "----\n*ARTIFACTS*")
        # Sample Raw log
        formatted_investigation_notes = formatted_investigation_notes.replace("SAMPLE RAW LOG:", "----\n*SAMPLE RAW LOGS*")
        formatted_investigation_notes = formatted_investigation_notes.replace("SAMPLE LOG", "----\n*SAMPLE RAW LOGS*")
        formatted_investigation_notes = formatted_investigation_notes.replace("Raw Log", "----\n*SAMPLE RAW LOGS*")
        formatted_investigation_notes = formatted_investigation_notes.replace("Log", "----\n*SAMPLE RAW LOGS*")
        # Others
        formatted_investigation_notes = formatted_investigation_notes.replace("*OSINT LINKS*", "----\n*OSINT LINKS*")
        """

        formatted_investigation_notes = markdownify.markdownify(formatted_investigation_notes, heading_style="ATX") 
        

        issue_dict = {
            'project': 'COR',
            'summary': investigation['title'],
            'description': formatted_investigation_notes,
            'issuetype': {'name': 'COR - Task'},
            'customfield_10683': { 'value' : investigation['severity']},
            'parent': {'key': 'COR-3099'},
        }

 
        new_issue = auth_jira.create_issue(fields=issue_dict)
        print_item("Jira Issue created <a href='{}/browse/{}'>{}</a>".format(jira_endpoint,new_issue,new_issue))
        logging.debug("Jira Issue created for {}/browse/{}".format(jira_endpoint,new_issue))
        new_tickets_mod_count = new_tickets_mod_count+1

        # brutal copy paste from jira-cor-enrich.py
        date_1 = datetime.datetime.strptime(new_issue.fields.created[:19], '%Y-%m-%dT%H:%M:%S')
        due_date = None
        if (str(new_issue.fields.customfield_10683) == 'Info'):
            due_date = date_1 + datetime.timedelta(days=240)
            priority = "Lowest"
        if (str(new_issue.fields.customfield_10683) == 'Low'):
            due_date = date_1 + datetime.timedelta(days=180)
            priority = "Low"
        if (str(new_issue.fields.customfield_10683) == 'Medium'):
            due_date = date_1 + datetime.timedelta(days=90)
            priority = "Medium"
        if (str(new_issue.fields.customfield_10683) == 'High'):
            due_date = date_1 + datetime.timedelta(days=30)
            priority = "High"
        if (str(new_issue.fields.customfield_10683) == 'Critical'):
            due_date = date_1 + datetime.timedelta(days=2)
            priority = "Critical"

        if (new_issue.fields.customfield_10683 == None and date_1.strftime('%Y-%m-%d') < '2021-11-03'):
            print_item('Issue {}: <strong>Max ovedue hit</strong>. Updating Issue Duedate. Created: {} Due:{} - Severity: {}'.format(new_issue.key, new_issue.fields.created, new_issue.fields.duedate, new_issue.fields.customfield_10683))
            logging.debug('Issue {}: <strong>Max ovedue hit</strong>. Updating Issue Duedate. Created: {} Due:{} - Severity: {}'.format(new_issue.key, new_issue.fields.created, new_issue.fields.duedate, new_issue.fields.customfield_10683))
            due_date = date_1 + datetime.timedelta(days=180)

        if(due_date != None):
            print_item('Updating Issue <a href="{}/browse/{}">{}</a> - Due:{} - Severity: {}'.format(jira_endpoint,new_issue.key,new_issue.key, new_issue.fields.duedate, new_issue.fields.customfield_10683))
            logging.debug('Updating Issue {}/browse/{} - Due:{} - Severity: {}'.format(jira_endpoint,new_issue.key, new_issue.fields.duedate, new_issue.fields.customfield_10683))
            new_issue.update(fields={'duedate': due_date.strftime('%Y-%m-%d')})

        new_issue.update(priority = {"name": priority})

        #Adding 'Jira Automation' comment - Appending AV reference
        panel_begin = "{panel:title=Automation - AlienValut Issue Imported:|bgColor=#e3fcef}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
        panel_ends = "{panel}"
        if (jira_executor_account_id == "5f7d69a13fe07600699920b8"): # If executor if Luca Bodini tag federico donati
            watcher_tag = "5d6e0cc74b5fce0db430cd77"
        else: # else tag Luca Bodini
            watcher_tag = "5f7d69a13fe07600699920b8"
        comment_body = panel_begin+"Internal investigation ticket for: {}/#/investigations/eu-central-1/{}".format(alienvault_endpoint, investigation['id'])+panel_ends
        comment = auth_jira.add_comment(new_issue, comment_body)
        auth_jira.add_watcher(new_issue, watcher_tag)

        # Below adding comment and changing investigation status on alienvault
        # changing status to 'In Review' status ID In Review can be seen in HTML code
        r = requests.get(investigation['_links']['self']['href'], headers=headers)
        investigation_info=json.loads(r.text)
        investigation_info['status']="In Review"
        investigation_info['description']=None
        del investigation_info['_links']
        r=requests.put(investigation['_links']['self']['href'], headers=headers, json=investigation_info )
        if (r.status_code == 200):
            print_item('Changed status of {}/#/investigations/eu-central-1/{} to <strong>"In Review"</strong> </li>'.format(alienvault_endpoint, investigation['id']))
            logging.debug('Changed status of {}/#/investigations/eu-central-1/{} to "In Review"'.format(alienvault_endpoint, investigation['id']))
        else:
            print_item_description('[-] Error status of {} cannot be changed'.format(investigation['_links']['self']['href']))
            print_item('[*] Exited with {} error code '.format(r.status_code))
            print_item('[*] Dump <pre>{}</pre>'.format(r.text))
            logging.error('Status of {} cannot be changed. Exited with {}. Dump: {}'.format(investigation['_links']['self']['href'], r.status_code,r.text))
        # Adding comment to the investigation
        message='Thanks Team, Internal Investigation Opened, Ref: {}/browse/{}'.format(jira_endpoint,new_issue.key)
        r=requests.post(investigation['_links']['notes']['href'], headers=headers, json={'investigationNumber': investigation['id'], 'message': message,} )
        if (r.status_code == 201):
            print_item('Adding comment to {}/#/investigations/eu-central-1/{} - {}'.format(alienvault_endpoint, investigation['id'], message))
            logging.debug('Adding comment to {}/#/investigations/eu-central-1/{}. {}'.format(alienvault_endpoint, investigation['id'], message))
        else:
            print_item_description('[-] Error comment to {}/#/investigations/eu-central-1/{} cannot be added'.format(alienvault_endpoint, investigation['id']))
            print_item('[-] Exited with {} error code '.format(r.status_code))
            print_item('[*] Dump <pre>{}</pre>'.format(r.text))
            logging.error('Status of {} cannot be changed. Exited with {}. Dump: {}'.format(investigation['id'], r.status_code,r.text))
        print_item_list_end()
    print_item_section('<p style="color:green;"><strong>Imported {} Issues in Jira from AlienVault Investigations.</strong></p>'.format(new_tickets_mod_count))
    logging.info('Imported {} Issues in Jira from AlienVault Investigations.'.format(new_tickets_mod_count))
print_item_list_end()
print_item_footer()
print_spacer()

################################################
# Closing investigations                       #
################################################
print_item_section("Closing AlienVault Investigations")
logging.info("Closing AlienVault Investigations")
close_investigations_mod_count=0
query="project = 'COR' AND parent=COR-3099 AND status IN ('False Positive', 'Fixed', 'Mitigated', 'Risk Accepted', 'Duplicate')"
for issue in auth_jira.search_issues(query, maxResults=0):
    av_investigation_number = None
    comments = auth_jira.comments(issue)
    for comment in comments:
        av_investigation_number = re.search(r'https://kaleyrainc.alienvault.cloud/#/investigations/eu-central-1/([a-zA-Z0-9-]+)', comment.body)
        if av_investigation_number != None:
            break

    av_investigation_number = av_investigation_number.group(1)

    if av_investigation_number == None:
        print_item_description("[-] FATAL: AlienValut Investigation Number Not found, for issue {}. Cannot continue the execution, please update the reference".format(issue))
        print_item_footer()
        print_spacer()
        print_footer()
        logging.critical("AlienValut Investigation Number Not found, for issue {}. Cannot continue the execution, please update the reference".format(issue))
        print("send_mail_true")
        quit()

    # If issue is in final state on jira, change the investigation status to closed
    r = requests.get('{}/investigations/v3/investigations/{}'.format(alienvault_investigations_endpoint, av_investigation_number), headers=headers)
    investigation_info=json.loads(r.text)
    if(investigation_info['status']!="Closed"):
        investigation_info['status']="Closed"
        investigation_info['description']=None
        del investigation_info['_links']
        r=requests.put('{}/investigations/v3/investigations/{}'.format(alienvault_investigations_endpoint, av_investigation_number), headers=headers, json=investigation_info )
        if (r.status_code == 200):
            print_item_description('Closing <a href="{}/#/investigations/eu-central-1/{}">investigation #{}</a>'.format(alienvault_endpoint, av_investigation_number,av_investigation_number))
            logging.debug('Closing {}/#/investigations/eu-central-1/{}'.format(alienvault_endpoint, av_investigation_number))
            print_item('Changing status of <a href="{}/#/investigations/eu-central-1/{}">investigation #{}</a> to <strong>"Closed"</strong> According to <a href="{}/browse/{}">{}</a> status </p>'.format(alienvault_endpoint, av_investigation_number, av_investigation_number, jira_endpoint, issue, issue))
            logging.debug('Changing status of {}/#/investigations/eu-central-1/{} to "Closed" According to {}/browse/{}'.format(alienvault_endpoint, av_investigation_number, jira_endpoint, issue))
            close_investigations_mod_count=close_investigations_mod_count+1
        else:
            print_item_description('[-] Error status of {} cannot be changed'.format(investigation['_links']['self']['href']))
            print_item('[*] Exited with {} error code '.format(r.status_code))
            print_item('<strong>[*] Dump </strong><pre>{}</pre>'.format(r.text))
            logging.error('Status of {} cannot be changed. {}'.format(investigation['_links']['self']['href'], r.text))
        print_item_list_end()
if (close_investigations_mod_count == 0):
    print_item_description('<p style="color:orange;"><strong>No changes detected on Jira.</strong></p>')
else:
    print_item_description('<p style="color:green;"><strong>Performed {} Modifications on AlienVault Investigations.</strong></p>'.format(close_investigations_mod_count))
logging.info('Performed {} Modifications on AlienVault Investigations.'.format(close_investigations_mod_count))
print_item_footer()
print_spacer()

################################################
# Sync @soc comments with AV                   #
################################################
print_item_section("Pushing @SOC Comments to AlienValut")
sync_comments_mod_count=0
query='project = "COR" AND parent=COR-3099'
for issue in auth_jira.search_issues(query, maxResults=0):
    av_investigation_number = None
    comments = auth_jira.comments(issue)
    for comment in comments:
        av_investigation_number = re.search(r'https://kaleyrainc.alienvault.cloud/#/investigations/eu-central-1/([a-zA-Z0-9-]+)', comment.body)
        if av_investigation_number != None:
            break

    av_investigation_number = av_investigation_number.group(1)

    if av_investigation_number == None:
        print_item_description("[-] FATAL: AlienValut Investigation Number Not found, for issue {}. Cannot continue the execution, please update the reference".format(issue))
        print_item_footer()
        print_spacer()
        print_footer()
        logging.critical("AlienValut Investigation Number Not found, for issue {}. Cannot continue the execution, please update the reference".format(issue))
        print("send_mail_true")
        quit()

    # once we have the av_investigation_number, iterating comments again to find @soc tags
    for comment in comments:
        if '@SOC' in str(comment.body) or '@soc' in str(comment.body):
            new_comment_no_soc_tag = comment.body
            new_comment_no_soc_tag = new_comment_no_soc_tag.replace("@soc", "")
            new_comment_no_soc_tag = new_comment_no_soc_tag.replace("@SOC", "")
            r=requests.post('{}/investigations/v3/investigations/{}/notes'.format(alienvault_investigations_endpoint, av_investigation_number), headers=headers, json={'message': new_comment_no_soc_tag,} )
            print(r.status_code)
            
            if (r.status_code == 201):
                print_item_description("Found New @SOC comment in <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, issue, issue))
                logging.debug("Found New @SOC comment in {}/browse/{}".format(jira_endpoint, issue))
                print_item("Adding comment to <a href='{}/#/investigations/eu-central-1/{}'>investigation {}</a></p>".format(alienvault_endpoint, av_investigation_number, av_investigation_number))
                print_item("<strong>Comment:</strong> {}".format(comment.body))
                logging.debug("Adding comment to {}/#/investigations/eu-central-1/{}: {}".format(alienvault_endpoint, av_investigation_number, comment.body))
                remove_soc_tag = auth_jira.comment(issue, comment)
                remove_soc_tag.update(body=new_comment_no_soc_tag)
                sync_comments_mod_count=sync_comments_mod_count+1
            else:
                print_item_description('[-] Error comment to {}/#/investigations/eu-central-1/{} cannot be added'.format(alienvault_endpoint, av_investigation_number))
                print_item('[-] Exited with {} error code '.format(r.status_code))
                print_item('<strong>[*] Dump </strong><pre>{}</pre>'.format(r.text))
                logging.error('Comment to {}/#/investigations/eu-central-1/{} cannot be added. Exited with {}. Dump: {}'.format(alienvault_endpoint, av_investigation_number, r.status_code, r.text))
            print_item_list_end()

if (sync_comments_mod_count == 0):
    print_item_description('<p style="color:orange;"><strong>No changes detected on Jira.</strong></p>')
else:
    print_item_description('<p style="color:green;"><strong>Performed {} Modifications on AlienVault Investigations.</strong></p>'.format(sync_comments_mod_count))
logging.info('Performed {} Modifications on AlienVault Investigations.'.format(sync_comments_mod_count))
print_item_footer()
print_spacer()
##############################################################
# Importing new SOC Operator comments for all investigations #
##############################################################

print_item_section("Pulling SOC operators comments into Jira")
logging.info("Pulling SOC operators comments into Jira")
soc_op_comments_mod_count=0
r = requests.post(alienvault_investigations_endpoint+'/investigations/v3/investigations/search', headers=headers, json={})
open_investigations=json.loads(r.text)
if not('investigations' in open_investigations):
    if r.status_code==401:
        print_item_description("Error 401 (Unauthorized): Invalid session cookie - Full authentication is required to access this resource")
        logging.critical("Error 401 (Unauthorized): Invalid session cookie. Full authentication is required to access this resource")
    else:
        print_item_description("<p style='color:orange;'><strong>No Investigation in 'Open' status has been found </strong></p>")
        logging.info("No Investigation in 'Open' status has been found ")
    print_item_footer()
    print_spacer()
    print_footer()
    print("send_mail_true")
    quit()

for investigation in open_investigations['investigations']:
    r = requests.get(alienvault_investigations_endpoint+'/investigations/v3/investigations/'+str(investigation['id'])+'/notes', headers=headers )
    investigation_notes=json.loads(r.text)

    if not('notes' in investigation_notes):
        print_item_description("Error 401 (Unauthorized): Invalid session cookie - Full authentication is required to access this resource")
        logging.critical("Error 401 (Unauthorized): Invalid session cookie. Full authentication is required to access this resource")
        print_item_footer()
        print_spacer()
        print_footer()
        print("send_mail_true")
        quit()

    if (len(investigation_notes['notes']) > 1):
        # Search cor tkt id in notes
        for i in range(len(investigation_notes['notes'])):
            cor_tkt_id = re.search(r'(COR-[0-9]+)', investigation_notes['notes'][i]['message'])
            if cor_tkt_id != None:
                break # exit loop when tkt id is found

    if cor_tkt_id == None:
        print_item_description("COR ticket id not found in previous comments of issue {}/#/investigations/eu-central-1/{} - {}".format(alienvault_endpoint, investigation['id'], investigation['title']))
        logging.critical("COR ticket id not found in previous comments of issue {}/#/investigations/eu-central-1/{} - {}".format(alienvault_endpoint, investigation['id'], investigation['title']))
        print_item_footer()
        print_spacer()
        print_footer()
        print("send_mail_true")
        quit()

    if (len(investigation_notes['notes']) > 1):
        # Search cor tkt id in notes
        for i in range(1, len(investigation_notes['notes'])):
            posted_comment = False
            soc_courtesy_comment_match = re.search(r'(COR-[0-9]+)', investigation_notes['notes'][i]['message'])
            if soc_courtesy_comment_match == None: #Comment is not 'Internal investigation opened [...]'
                comments = auth_jira.comments(cor_tkt_id.group(1))
                for comment in comments:
                    posted_comment_match = re.search(investigation_notes['notes'][i]['id'], comment.body)
                    if posted_comment_match != None:
                        posted_comment = True
                if posted_comment == False and (investigation_notes['notes'][i]['created']['by'] not in kaleyra_sec_team):
                    panel_begin = "{panel:title=Automation - SOC Operator Added Comment To This Investigation:|bgColor=#eae6ff}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
                    panel_ends = "{panel}"
                    comment_body = panel_begin+investigation_notes['notes'][i]['message']+"\n\nAlienVault Comment id: "+investigation_notes['notes'][i]['id']+panel_ends
                    comment_body = markdownify.markdownify(comment_body, heading_style="ATX")
                    if len(comment_body)>32767:
                        comment_body=comment_body[:32500]+"\n\Comment too long. Full Description on Alienvault"+"\n\nAlienVault Comment id: "+investigation_notes['notes'][i]['id']
                    comment = auth_jira.add_comment(cor_tkt_id.group(1), comment_body)
                    print_item_description("Found New SOC operator comment in investigation <a href='{}/#/investigations/eu-central-1/{}'>investigation {}</a> {}".format(alienvault_endpoint, investigation['id'], investigation['id'],investigation['title']))
                    logging.debug("Found New SOC operator comment in investigation {}/#/investigations/eu-central-1/{}. {}".format(alienvault_endpoint, investigation['id'],investigation['title']))
                    print_item("Adding SOC Operator comment in <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, cor_tkt_id.group(1), cor_tkt_id.group(1) ))
                    print_item("<strong>Comment:</strong> {}".format(investigation_notes['notes'][i]['message']))
                    logging.debug("Adding SOC Operator comment in {}/browse/{}. {}".format(jira_endpoint, cor_tkt_id.group(1), investigation_notes['notes'][i]['message']))
                    soc_op_comments_mod_count = soc_op_comments_mod_count+1
                    print_item_list_end()
if (soc_op_comments_mod_count == 0):
    print_item_description('<p style="color:orange;"><strong>No changes detected on AlienVault.</strong></p>')
else:
    print_item_description('<p style="color:green;"><strong>Performed {} Modifications on Jira Tickets.</strong></p>'.format(soc_op_comments_mod_count))
logging.info('Performed {} Modifications on Jira Tickets.'.format(soc_op_comments_mod_count))
print_item_list_end()
print_item_footer()
print_spacer()
print_counter_four(new_tickets_mod_count, "New Tickets", close_investigations_mod_count, "Closed Investigations", sync_comments_mod_count, "Pushed Comments", soc_op_comments_mod_count, "SOC Operators Comments Pulled" )
print_footer()

logging.info("COR AlienVault sync investigations ending procedure")
logging.info("Execution summary:")
logging.info("New Tickets {}".format(new_tickets_mod_count))
logging.info("Closed Investigations {}".format(close_investigations_mod_count))
logging.info("Pushed Comments {}".format(sync_comments_mod_count))
logging.info("SOC Operators Comments Pulled {}".format(soc_op_comments_mod_count))

if (sync_comments_mod_count > 0 or close_investigations_mod_count > 0 or new_tickets_mod_count > 0 or soc_op_comments_mod_count > 0):
    print("send_mail_true")