# required creds : jira API, GSuite App Password, Github Access Token
from github import Github
import requests
import json
import re
import time
from itertools import tee
from jira import JIRA
from htmlMailGenerator import *

github_access_token = '{{ github_access_token }}'
jira_endpoint='https://kaleyra.atlassian.net'
user='{{ username }}'
user_mail=user+'@kaleyra.com'
jira_user_api_token='{{ jira_user_api_token }}'
jira_executor_account_id='{{ jira_executor_account_id }}' # Luca Bodini : 5f7d69a13fe07600699920b8
                                                    # Federico Donati : 5d6e0cc74b5fce0db430cd77
jira = JIRA(server=jira_endpoint, basic_auth=(user_mail, jira_user_api_token))
git = Github(github_access_token)

dry_run = {{ dry_run }}

# Template part ends here

# Assignee
# Vijay Kumar Reddy : 6005265ebe0f980076bd2fe1
# Aman Jain : 557058:30b77422-b2dc-4665-8310-0f91ea586d06

targets = [{
                'domain': 'alerts.solutionsinfini.com',
                'keyRegex': r'($|&|\?|\'|"|\ |=)(\w{33})($|&|\?|\'|"|\ )',
                'assignee' : '712020:32a1231d-6d1b-4dbc-a31d-693eba888fc3'
            },
            {
                'domain': 'kaleyra.io',
                "keyRegex": r'($|&|\?|\'|"|\ |=)(\w{33})($|&|\?|\'|"|\ )',
                'assignee' : '712020:32a1231d-6d1b-4dbc-a31d-693eba888fc3'
            },
            {
                'domain': 'voice.kaleyra.com',
                "keyRegex": r'($|&|\?|\'|"|\ |=)(\w{33})($|&|\?|\'|"|\ )',
                'assignee' : '712020:32a1231d-6d1b-4dbc-a31d-693eba888fc3'
            }]

print_head()
print_header()

if dry_run:
    print_title("<h2>GitHub OSINT - Leaked API Keys Lookup Executed in <strong style='color:orange;'>Dry Run Mode</strong>!</h2>")
else:
    print_title("<h2>GitHub OSINT - Leaked API Keys Lookup Executed</h2>")

print_subtitle("Findings Details:")


# Get all jira issues in order to do not create duplicates
known_leaked_sources = dict([])
query = 'parent=COR-1908'
issues = jira.search_issues(query, maxResults=0)
for issue in issues:
    known_leaked_sources[str(issue.fields.summary)] = str(issue.key)

mod_count=0
for target in targets:
    hits = git.search_code(target['domain'])
    print_item_section("Found <strong>{} hit(s)</strong> for {}</h3>".format(hits.totalCount, target['domain']))

    for hit in hits:
        time.sleep(10)
        affected_keys_message = ""
        r = requests.get(hit.download_url)
        affected_code = r.text
        matches = re.finditer(target['keyRegex'], affected_code, re.MULTILINE)
        matches, control_match = tee(matches)
        if (len(list(control_match))!=0):
            affected_keys_message = "Found match on file {} \n".format(hit.html_url)
            print_item_description("Found match on <a href='{}'>GitHub file</a>".format(hit.html_url))

            for match in matches:
                start = match.span()[0]
                line_no = affected_code[:start].count("\n")
                f = open("/tmp/leaked_keys.list", "a")
                f.write(match.group(0))
                f.close()
                leaked_api_key = match.group(0)[:-7]+"*******"
                leaked_api_key = re.sub(r'($|&|\?|\'|"|\ |=)', '',leaked_api_key)
                affected_keys_message = affected_keys_message + "Found possible api key {} leaked on line {} \n".format(leaked_api_key, line_no+1)
                print_item("Found possible leaked api key {} on <strong>line {} </strong>".format(leaked_api_key, line_no+1))

            description = '*Observation:* \n\
                           Please notice that the developer listed in this issue’s summary is disclosing on github an API key for *'+target['domain']+'* .\n \
                           This can allow an attacker with simple OSINT techniques to impersonate this user and consume credits without the account owner permission.\n \
                           \n\
                           ---- \n\
                           *Remediation:* \n \
                           It is recommended to revoke The API key disclosed in code and inform the user about the leakage.\n\
                           ---- \n\
                           *Severity:* {color:red} *High* {color} \n\
                           ---- \n\
                           *Affected Keys:* \n\
                           '+affected_keys_message

            issue_dict = {
                'project': 'COR',
                'summary': hit.html_url,
                'description': description,
                'issuetype': {'name': 'COR - Subtask'},
                'customfield_10683': { 'value' : 'High'},
                'parent': {'key': 'COR-1908'},
                'priority': {'name': 'High'},
                'assignee' : {'accountId': target['assignee']}
            }

            if (hit.html_url not in known_leaked_sources):
                if dry_run:
                    new_issue = 'DRY_RUN_MODE'
                else:
                    new_issue = jira.create_issue(fields=issue_dict)
                mod_count=mod_count+1
                print_item("Discovered a <strong style='color:green;'>new leakage hit</strong>, opened <a href='{}/browse/{}'>{}</a></p>".format(jira_endpoint, new_issue, new_issue))
                print_item_list_end()
            else:
                issue_id = known_leaked_sources[hit.html_url]
                query = 'parent=COR-1908 AND issue={}'.format(issue_id)
                issues = jira.search_issues(query, maxResults=1)
                issue = issues[0]
                if(str(issue.fields.status) not in ["False Positive", "Fixed", "Duplicate"]):
                    # Retreive watchers list and build a string to append at the bottom of a comment
                    watchers_tag="+ "
                    issue_watchers = jira.watchers(issue).watchers
                    for issue_watcher in issue_watchers:
                        if(str(issue_watcher.accountId)!=jira_executor_account_id):
                            watchers_tag+="[~accountid:{}] ".format(issue_watcher.accountId)
                    panel_begin = "{panel:title=API Key still available online!|bgColor=#fefae6}" #panel types: https://community.atlassian.com/t5/Jira-questions/Markdown-for-info-panel-in-Jira-new-issue-view/qaq-p/1183207
                    panel_ends = "{panel}"
                    if (issue.fields.assignee == None):
                        assignee = "Team \n"
                    else:
                        assignee = "[~accountid:{}] \n".format(issue.fields.assignee.accountId)

                    if dry_run:
                        print_item("<a href='{}'>Analyzed source</a> has <strong style='color:orange;'>already been hit by the scanner</strong>, real run would ping the assignee on jira ticket <a href='{}/browse/{}'>{}</a>".format(hit.html_url, jira_endpoint ,issue,issue))
                    else:
                        comment_header = "Hi {}".format(assignee)
                        comment_body = "Please notice that this api key is still leaked and publicly available on: {} \n please *revoke this leaked API key* and inform the customer as soon as possible \n\n Thank you! \n".format(hit.html_url)
                        comment = jira.add_comment(issue, panel_begin+comment_header+comment_body+watchers_tag+panel_ends)
                        print_item("<a href='{}'>Analyzed source</a> has <strong style='color:orange;'>already been hit by the scanner</strong>, pinging assignee on jira ticket <a href='{}/browse/{}'>{}</a>".format(hit.html_url, jira_endpoint ,issue,issue))
                    print_item_list_end()
                else:
                    if(str(issue.fields.status)=="False Positive"):
                        print_item("<a href='{}'>Analyzed source</a> has <strong style='color:orange;'>already been marked as false positive. </strong> issue has been tracked on <a href='{}/browse/{}'>{}</a>".format(hit.html_url, jira_endpoint ,issue, issue))
                        print_item_list_end()
                    else: # Status is fixed
                        fixed_known_api_key_matches = re.finditer(r'((\w{27}|\w{26})\*{7})', issue.fields.description, re.MULTILINE)
                        fixed_known_api_key_matches, control_fixed_known_api_key_matches = tee(fixed_known_api_key_matches)
                        matches_no = len(list(control_fixed_known_api_key_matches))
                        known_leaked_api_no = 0
                        if (matches_no==0):
                            print_item("<a href='{}'>Analyzed source</a> is a known leakage source but <strong style='color:orange;'>ticket does not contain any exportable reference to leaked API key in code</strong> <a href='{}/browse/{}'>{}</a> creating a new issue, please if the API key is the same, report all the backlog and delete the old issue.</p>".format(hit.html_url, jira_endpoint ,issue, issue))
                            if dry_run:
                                new_issue = 'DRY_RUN_MODE'
                            else:
                                new_issue = jira.create_issue(fields=issue_dict)
                            mod_count=mod_count+1
                            print_item("Opening a <strong style='color:green;'>new issue</strong> <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, new_issue,new_issue))
                        else:
                            for fixed_known_api_key in fixed_known_api_key_matches:
                                if (fixed_known_api_key.group(0) == leaked_api_key):
                                    print_item("<a href='{}'>Analyzed source</a> has <strong style='color:orange;'>already been disabled</strong>, ticket marked as fixed: <a href='{}/browse/{}'>{}</a>".format(hit.html_url, jira_endpoint ,issue, issue))
                                else:
                                    if dry_run:
                                        new_issue = 'DRY_RUN_MODE'
                                    else:
                                        new_issue = jira.create_issue(fields=issue_dict)
                                    mod_count=mod_count+1
                                    print_item("Discovered a <strong style='color:green;'>new leakage hit in an already probed repository</strong>, opening a new jira issue <a href='{}/browse/{}'>{}</a>".format(jira_endpoint, new_issue, new_issue))
                        print_item_list_end()
    print_item_list_end()
    print_item_footer()
    print_spacer()

print_counter_mono(mod_count, "New Leakage Hits")
print_footer()
print('send_mail_true')
