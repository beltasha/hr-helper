import csv

csvfile_stat = open('../datasets/GH_user_statistic_prepared.csv', 'w', newline='')
fieldnames_stat = [
    'login',
    'SO_id',
    'followers_count',
    'following_count',
    'repositories_count', 
    'fork_count', 
    'star_count',
    'closed_pr_count',
    'merged_pr_count',
    'all_pr_count',
    'commit_count',
    'success_merge_status_num',
    'fail_merge_status_num',
    'SO_reputation'
  ]
writer_stat = csv.DictWriter(csvfile_stat, fieldnames=fieldnames_stat)
writer_stat.writeheader()

with open('../datasets/GH_user_statistic.csv', 'r') as csvfile:
  zero_status_num = 0
  reader = csv.DictReader(csvfile)
  for row in reader:
    if row['success_merge_status_num'] == '0' and row['fail_merge_status_num'] == '0':
      print('zero!')
      zero_status_num += 1
    else:
      writer_stat.writerow(row)

  print('zero_status_num')
  print(zero_status_num)
    