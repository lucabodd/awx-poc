from htmlMailGenerator import *

print_head()
print_header()
print_title("{{ cluster_name | upper }} user access enumeration for {{ year_quarter.stdout }}")
print_subtitle('New reports generated for {{ cluster_name | upper}}, {{ year_quarter.stdout }}')
print_item_section("Schedule executed {{ ansible_date_time.date }} {{ ansible_date_time.hour }}:{{ ansible_date_time.minute }}:{{ ansible_date_time.second }} report is available is available here: <a href='https://reports.awx.hqit.kaleyra.com:8080/secops/reports/enumerate-user-access/{{year_quarter.stdout}}/{{cluster_name}}'>{{ cluster_name | upper}} Report</a>")
print_item_footer()
print_spacer()
print_footer()
print("send_mail_true")
