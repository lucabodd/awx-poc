## API token eYdNIit5NJvdtZFYYeHO4716
# Secerity : issue.fields.customfield_10683
# CreationDate: issue.fields.created
# DueDate: issue.fields.created
# IssueId : issue.key
# Assignee: issue.fields.assignee
# Assignee AccountId: issue.fields.assignee.accountId

import datetime
from datetime import date
import json
import re
import sys
from pprint import pprint
from htmlMailGenerator import *

from jira import JIRA

jira_endpoint='https://kaleyra.atlassian.net'
user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))
executor_account_id='{{ jira_executor_account_id }}' # Luca Bodini : 5f7d69a13fe07600699920b8
                                               # Federico Donati : 5d6e0cc74b5fce0db430cd77
kaleyra_sec_team_jira_ids = ['5f7d69a13fe07600699920b8', '5d6e0cc74b5fce0db430cd77']
jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))

query = """ {{jql_query}} """

print_head()
print_header()
print_title("Jira - COR, spam overdue tickets")
print_subtitle("Annoying people to get the job done!")

print_item_section('Adding comment for each match of query')
mod_count=0
for issue in jira.search_issues(query, maxResults=0):
    # Retreive watchers list and build a string to append at the bottom of a comment
    watchers_tag=""
    issue_watchers = jira.watchers(issue).watchers
    for issue_watcher in issue_watchers:
        if(str(issue_watcher.accountId) not in kaleyra_sec_team_jira_ids):
            watchers_tag+="[~accountid:{}] ".format(issue_watcher.accountId)
    panel_begin = "{panel:title=Jira Overdue Tickets Automation.|bgColor=#deebff}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
    if (issue.fields.assignee != None):
        comment_header = "Hi [~accountid:{}] \n".format(issue.fields.assignee.accountId)
    else:
        comment_header = "Hi [~accountid:{}] \n".format(executor_account_id)
    comment_body = "This issue is overdue and will be part of the next vulnerability management review meeting"+"\n"
    panel_ends = "{panel}"
    comment = jira.add_comment(issue, panel_begin+comment_header+comment_body+watchers_tag+panel_ends)
    mod_count=mod_count+1
    print_item_description('Adding comment to issue <a href="{}/browse/{}">{}</a>'.format(jira_endpoint, issue.key, issue.key))
    print_item("Due Date: {}, Severity: {}, Created on: {}".format(issue.fields.duedate, issue.fields.customfield_10683,issue.fields.created))
    print_item_list_end()
    
if (mod_count == 0):
    print_item_description('<p style="color:orange;"><strong>No comments added, check if the query returns any result.</strong></p>')

print_item_footer()
print_spacer()
print_counter_mono(mod_count, "Tickets Spammed")
print_footer()
print('send_mail_true')
