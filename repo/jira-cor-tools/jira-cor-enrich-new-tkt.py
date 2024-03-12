import datetime
import json
from jira import JIRA
from htmlMailGenerator import *

jira_endpoint='https://kaleyra.atlassian.net'
user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))
query='project = "COR" AND issuetype!="COR - Epic" AND createdDate>="-30d" AND (labels != Parent-Issue or labels is EMPTY) AND duedate IS EMPTY'

print_head()
print_header()
print_title("Jira - COR, Enrich New Tickets")
print_subtitle("Schedule executed {{ ansible_date_time.date }} {{ ansible_date_time.hour }}:{{ ansible_date_time.minute }}:{{ ansible_date_time.second }}")
print_item_section('Adding additional information to newly created tickets')
mod_count=0
warnings_count=0
for issue in auth_jira.search_issues(query, maxResults=0):
    if(issue.fields.customfield_10683 == None):
        print_item_description("Ticket <a href='{}/browse/{}'>{}</a> does not have severity field set.".format(jira_endpoint, issue, issue))
        print_item_list_end()
        warnings_count=warnings_count+1
        continue
    print_item_description('Looking Into Issue <a href="{}/browse/{}">{}</a> severity: {}'.format(jira_endpoint, issue, issue, issue.fields.customfield_10683))
    date_1 = datetime.datetime.strptime(issue.fields.created[:19], '%Y-%m-%dT%H:%M:%S')
    due_date = None
    if (str(issue.fields.customfield_10683) == 'Info'):
        due_date = date_1 + datetime.timedelta(days=240)
        priority = "Lowest"
    if (str(issue.fields.customfield_10683) == 'Low'):
        due_date = date_1 + datetime.timedelta(days=180)
        priority = "Low"
    if (str(issue.fields.customfield_10683) == 'Medium'):
        due_date = date_1 + datetime.timedelta(days=90)
        priority = "Medium"
    if (str(issue.fields.customfield_10683) == 'High'):
        due_date = date_1 + datetime.timedelta(days=30)
        priority = "High"
    if (str(issue.fields.customfield_10683) == 'Critical'):
        due_date = date_1 + datetime.timedelta(days=2)
        priority = "Critical"

    if (issue.fields.customfield_10683 == None and date_1.strftime('%Y-%m-%d') < '2021-11-03'):
        print_item('Max ovedue hit. Updating Issue Duedate. Updating Issue Due Date {}'.format(due_date))
        due_date = date_1 + datetime.timedelta(days=180)

    if(due_date != None):
        print_item('Updating Issue Due Date {}'.format(due_date))
        issue.update(fields={'duedate': due_date.strftime('%Y-%m-%d')})

    issue.update(priority = {"name": priority})
    mod_count=mod_count+1
    print_item('Updating Issue Priority: {}'.format(issue.fields.priority))
    print_item_list_end()
print_item_footer()
print_spacer()
print_counter_two(mod_count, "Tickets Updated", warnings_count, "Warnings Generated")
print_footer()
if(mod_count>0 or warnings_count>0):
    print('send_mail_true')
