from jira import JIRA
from datetime import date
import csv
from htmlMailGenerator import *
#import logging

version="1.1.0"

user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
jira_executor_account_id='{{ jira_executor_account_id }}' # Luca Bodini : 5f7d69a13fe07600699920b8
                                                    # Federico Donati : 5d6e0cc74b5fce0db430cd77
kaleyra_sec_team=['luca.bodini@kaleyra.com', 'federico.donati@kaleyra.com']
jira_endpoint='https://kaleyra.atlassian.net'
auth_jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))

#today = date.today()
#logging.basicConfig(level=logging.WARNING,
#                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                    datefmt='%m-%d %H:%M',
#                    filename='/tmp/awx-cor-management-review-sync'+str(today)+'.log')

print_head()
print_header()
print_title("COR - Alienvault Management Review Meeting Sync")
print_subtitle("Schedule executed {{ ansible_date_time.date }} {{ ansible_date_time.hour }}:{{ ansible_date_time.minute }}:{{ ansible_date_time.second }}")

print_item_section("Syincing comments")

changes=0

try:
    with open('/tmp/file.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='	')
        for issue_mgmt_comment in spamreader:
            panel_begin = "{panel:title=Automation - Management Review Meeting Decision:|bgColor=#deebff}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
            panel_ends = "{panel}"
            comment_body = issue_mgmt_comment[1]
            print_item_description("Adding comment to <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, issue_mgmt_comment[0], issue_mgmt_comment[0] ))
            print_item("<strong>Comment:</strong> {}".format(comment_body))
            comment = auth_jira.add_comment(issue_mgmt_comment[0], panel_begin+comment_body+panel_ends)
            changes=changes+1
            print_item_list_end()
    
    if (changes == 0):
        print_item_description('<p style="color:orange;"><strong>No changes detected on file.</strong></p>')
    else:
        print_item_description('<p style="color:green;"><strong>Performed {} Modifications on Jira Tickets.</strong></p>'.format(changes))
        print("send_mail_true")
        
    print_item_list_end()
    print_item_footer()
    print_spacer()
    print_counter_mono(changes, "Comments Added")
    print_footer()

except IOError:
    print_item_description('Error /tmp/file.csv cannot be found')
    print_item_list_end()
    print_item_footer()
    print_spacer()
    print_footer()
