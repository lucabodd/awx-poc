#* Relay Board: issue.fields.customfield_11464 - new customfield_11464
#* Relay Subject: issue.fields.customfield_11465 - new customfield_11465
#* Relay Description: issue.fields.customfield_11466 - new customfield_11466


import datetime
import json
from jira import JIRA
from htmlMailGenerator import *

user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
jira_executor_account_id='{{ jira_executor_account_id }}' # Luca Bodini : 5f7d69a13fe07600699920b8
                                                    # Federico Donati : 5d6e0cc74b5fce0db430cd77
kaleyra_sec_team=['luca.bodini@kaleyra.com', 'federico.donati@kaleyra.com']
jira_endpoint='https://kaleyra.atlassian.net'
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))

# Template Part Ends

project_defaults = {
    'CE': {"issuetype": {"name" : "Task"}},
    'CLOUDENGG': {"issuetype": {"name" : "Task"}},
    'CLOUDOPS': {"issuetype": {"name" : "Task"}},
    'DBOPS': {"issuetype": {"name" : "Task"}, "customfield_11451": {"value" : "K.io & Legacy", "child": {"value": "All"}}, "customfield_11452": [{"value" : "Prod"}], "customfield_11453": [{"value" : "All"}], "labels": ["Infosec"]},
    'DCOPS': {"issuetype": {"name" : "Task"}, "customfield_11481": {"value": "Config", "child": { "value" : "Security Policies" } }},
    'DEVOPS': {"issuetype": {"name" : "Task"}},
    'GWSRE': {"issuetype": {"name" : "Task"}},
    'INFRAOPS': {"issuetype": {"name" : "Task"}},
    'SECOPS':{"issuetype": {"name" : "Task"}},
    'SREBFSIOPS': {"issuetype": {"name" : "Task"}},
    'TECHOPS': {"issuetype": {"name" : "Task"}},
    'VI': {"issuetype": {"name" : "Task"}},
    'VOICE': {"issuetype": {"name" : "Task"}, "labels": ["SECOPS"]},
    'VIDEOOPS': {"issuetype": {"name" : "Task"}},
    'VOICEOPS': {"issuetype": {"name" : "Task"}}
}

print_head()
print_header()
print_title("Jira - SECOPS, External Relay Board Sync")
print_subtitle("Schedule executed {{ ansible_date_time.date }} {{ ansible_date_time.hour }}:{{ ansible_date_time.minute }}:{{ ansible_date_time.second }}")

query='project = "SECOPS" AND issuetype!="Epic" AND ("Relay Board" IS NOT EMPTY) AND ("Relay Description" IS NOT EMPTY) AND ("Relay Summary" IS NOT EMPTY)'
print_item_section('Syncing tickets with Relay Board field set')
mod_count=0
for issue in auth_jira.search_issues(query, maxResults=0):
    print_item_description("Found ticket <a href='{}/browse/{}'>{}</a>, forwarding to: {}".format(jira_endpoint, str(issue), str(issue), str(issue.fields.customfield_11464)))

    if(str(issue.fields.customfield_11465).lower().strip() == "mirror"):
        new_issue_summary = str(issue.fields.summary)
    else:
        new_issue_summary = str(issue.fields.customfield_11465)

    if(str(issue.fields.customfield_11466).lower().strip() == "mirror"):
        new_issue_description = str(issue.fields.description)
    else:
        new_issue_description = str(issue.fields.customfield_11466)



    issue_dict = {
            'reporter': { "id": issue.fields.reporter.accountId },
            'project': str(issue.fields.customfield_11464),
            'summary': new_issue_summary,
            'description': new_issue_description,
            'priority': {'name': str(issue.fields.priority)}
    }

    issue_dict.update(project_defaults[str(issue.fields.customfield_11464)])
    if str(issue.fields.customfield_11464) in ["DCOPS", "TECHOPS"]: issue_dict.pop('reporter') 
    new_issue = auth_jira.create_issue(fields=issue_dict)

    print_item("Created a new issue in the external board: <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, new_issue, new_issue))
    if (jira_executor_account_id == "5f7d69a13fe07600699920b8"): # If executor if Luca Bodini tag federico donati
            watcher_tag = "5d6e0cc74b5fce0db430cd77"
    else: # else tag Luca Bodini
            watcher_tag = "5f7d69a13fe07600699920b8"
    auth_jira.add_watcher(new_issue, watcher_tag)

    panel_begin = "{panel:title=Jira Automation:|bgColor=#deebff}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
    panel_ends = "{panel}"
    comment_text="This ticket is related to {}/browse/{}.\nYou can find additional information on the abovementioned ticket related to this observation.".format(jira_endpoint, issue)
    comment_body = panel_begin+comment_text+panel_ends
    comment = auth_jira.add_comment(new_issue, comment_body)

    auth_jira.create_issue_link(type='relates to', inwardIssue=str(new_issue), outwardIssue=str(issue))
    mod_count=mod_count+1

    panel_begin = "{panel:title=Jira Automation:|bgColor=#deebff}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
    panel_ends = "{panel}"
    comment_text="Opened ticket on external board {}/browse/{}.\nYou can find additional information on the abovementioned ticket related to this observation.".format(jira_endpoint, new_issue)
    comment_body = panel_begin+comment_text+panel_ends
    comment = auth_jira.add_comment(issue, comment_body)
    issue.update(fields={'customfield_11464': None, 'customfield_11465': None, 'customfield_11466': None})
    print_item_list_end()
if (mod_count == 0):
    print_item_description('<p style="color:orange;"><strong>No changes detected on Jira.</strong></p>')
else:
    print_item_footer()
    print_spacer()
    print_counter_mono(mod_count, "External Tickets Opened")
    print_footer()
    print('send_mail_true')
