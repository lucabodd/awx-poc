# Jira Attributes
## COR - Attributes list
* Severity : issue.fields.customfield_10683
* CreationDate: issue.fields.created
* DueDate: issue.fields.created
* IssueId : issue.key
* Assignee: issue.fields.assignee
* Assignee AccountId: issue.fields.assignee.accountId
* Priority: issue.fields.priority
* Relay Board: issue.fields.customfield_11417
* Relay Subject: issue.fields.customfield_11419
* Relay Description: issue.fields.customfield_11418

## SECOPS - Attributes list
* Relay Board: issue.fields.customfield_11464
* Relay Subject: issue.fields.customfield_11465
* Relay Description: issue.fields.customfield_11466


## Code Snippet to retreive attribute list
```
for field_name in issue.raw['fields']:
    print("Field:", field_name, "Value:", issue.raw['fields'][field_name])
```
