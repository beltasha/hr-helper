import re
import csv
# result = re.match(r"^.*github.com/([^\"\/]+)", '<row Id="5542851" Reputation="1" CreationDate="2015-11-09T14:45:22.000" DisplayName="Alvaro Carneiro" LastAccessDate="2016-09-08T11:21:42.790" WebsiteUrl="https://github.com/alv-c/wewe" Location="Montevideo, Montevideo Department, Uruguay" AboutMe="&lt;p&gt;Developer just for fun â„¢&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Want to create all; Want to destroy all&lt;/p&gt;&#xA;" Views="0" UpVotes="0" DownVotes="0" ProfileImageUrl="https://lh4.googleusercontent.com/-f52iJHmHTQI/AAAAAAAAAAI/AAAAAAAAABg/0UeYzsigA48/photo.jpg?sz=128" AccountId="5911853" />')
# print(result)
# if (result):
#   print(result.group(1))

def extract_github_logins(writer): 
  fp = open('../SOusers/Users.xml', encoding='utf8')
  for i, line in enumerate(fp):
    if i == 0 or i == 1:
      continue
    GH_login_match = re.match(r"^.*github.com/([^\"\/&]+)", line)
    SO_id_match = re.match(r"^.*row Id=\"(\d+)", line)
    SO_reputation_match = re.match(r"^.*Reputation=\"(\d+)", line)
    
    if (GH_login_match):
      GH_login = GH_login_match.group(1)
      SO_id = SO_id_match.group(1)
      SO_reputation = SO_reputation_match.group(1)
      try:
        writer.writerow({'GH_login': GH_login, 'SO_id': SO_id, 'SO_reputation': SO_reputation})
        # print(GH_login, SO_id, SO_reputation)
      except:
        print('Error!')
      
  fp.close()

with open('hr_helper.csv', mode='a+', newline='') as csv_file:
  fieldnames = ['GH_login', 'SO_id', 'SO_reputation']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
  writer.writeheader()
  extract_github_logins(writer)