import csv
import requests
import time
import config
from urllib.parse import urlparse

authorization_token = "Bearer {0}".format(config.TOKEN)
headers = {"Authorization": authorization_token}

def run_query(query, variables):
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def get_query(login, repositories_count, pull_request_count, commit_count):
  query = '''
		query($login: String!, $repositories_count: Int!, $pull_request_count: Int!, $commit_count: Int!) { 
      user(login: $login) {
        followers {
          totalCount
        }
        following {
          totalCount
        }
        repositories (last: $repositories_count){
          totalCount
          nodes {
            name,
            forkCount,
            stargazers {
              totalCount
            },
            closedPullRequests: pullRequests (states:CLOSED){
              totalCount
            },
            mergedPullRequests: pullRequests (states:MERGED){
              totalCount
            },
            allPullRequests: pullRequests(last: $pull_request_count) {
              totalCount,
              nodes {
                commits {
                  totalCount
                }
              }
            },
          }
        }
        contributionsCollection {
        contributionCalendar {
            totalContributions,
        }
        pullRequestContributions(last:$pull_request_count) {
          nodes {
            pullRequest {
              url,
              commits (last: $commit_count) {
                nodes {
                  commit {
                    commitUrl,
                    status {
                      state,
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
	}'''
  variables = {
    'login' : login,
    'repositories_count' : repositories_count,
    'pull_request_count': pull_request_count,
    'commit_count': commit_count
  }

  return query, variables

def calculate_user_info(login, userData):
  try:
    fork_count = 0
    star_count = 0
    closed_pr_count = 0
    merged_pr_count = 0
    all_pr_count = 0
    commit_count = 0
    repositories = userData['repositories']['nodes']
    for repository in repositories:
      fork_count += repository['forkCount']
      star_count += repository['stargazers']['totalCount']
      closed_pr_count += repository['closedPullRequests']['totalCount']
      merged_pr_count += repository['mergedPullRequests']['totalCount']
      all_pr_count += repository['allPullRequests']['totalCount']
      
      pullRequests = repository['allPullRequests']['nodes']
      for pullRequest in pullRequests:
        commit_count += pullRequest['commits']['totalCount']
    return {
      'login': login,
      'followers_count': userData['followers']['totalCount'],
      'following_count': userData['following']['totalCount'],
      'repositories_count': userData['repositories']['totalCount'],
      'fork_count': fork_count,
      'star_count': star_count,
      'closed_pr_count': closed_pr_count,
      'merged_pr_count': merged_pr_count,
      'all_pr_count': all_pr_count,
      'commit_count': commit_count
    }
  except: 
    print('error in "calculate_user_info"')

def calculate_merge_status_data(login, contribution_pull_requests):
  rows_info = []
  success_num = 0
  fail_num = 0
  SUCCESS_STATUS = 'SUCCESS'
  FAIL_STATUS = 'FAILURE'
  try:
    for contribution_pull_request in contribution_pull_requests:
        repo = contribution_pull_request['pullRequest']['url'].split('/')[-3]
        pull_request = contribution_pull_request['pullRequest']['url'].split('/')[-1]
        commits = contribution_pull_request['pullRequest']['commits']['nodes']
        for contribution_commit in commits:
          if (contribution_commit['commit']['status'] != None):
            commit = contribution_commit['commit']['commitUrl'].split('/')[-1]
            status = contribution_commit['commit']['status']['state']
            if status == SUCCESS_STATUS:
              success_num += 1
            if status == FAIL_STATUS:
              fail_num += 1 
            rows_info.append({
              'login': login,
              'repo': repo, 
              'pullRequest': pull_request,
              'commit': commit, 
              'status': status
            })
  except SyntaxError as error:
    print(error)
  except:
    print('error in "calculate_merge_status_data"')
  return {'rows_info': rows_info, 'merge_statistics': {'success_num': success_num, 'fail_num': fail_num}}

def calculate(login, repositories_count, pull_request_count, commit_count):
  query, variables = get_query(login, repositories_count, pull_request_count, commit_count)
  result = run_query(query, variables)

  try:
    contribution_pull_requests = result['data']['user']['contributionsCollection']['pullRequestContributions']['nodes']
    merge_status_data = calculate_merge_status_data(login, contribution_pull_requests)
    user_data = calculate_user_info(login, result['data']['user'])
  except SyntaxError as error:
    print(error)
  except:
    print('Something wrong with data')

  return { 'merge_status_data': merge_status_data, 'user_data': user_data }


def main():
  repositories_count = 30
  pull_request_count = 20
  commit_count = 20
  
  csvfile_merge_stat = open('../datasets/GH_merge_status_statisitic.csv', 'a+', newline='')
  fieldnames_merge_stat = ['login', 'repo', 'pullRequest', 'commit', 'status']
  writer_merge_info = csv.DictWriter(csvfile_merge_stat, fieldnames=fieldnames_merge_stat)
  writer_merge_info.writeheader()

  csvfile_stat = open('../datasets/GH_user_statistic.csv', 'a+', newline='')
  fieldnames_stat = [
    'login',
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
    'fail_merge_status_num'
  ]
  writer_stat = csv.DictWriter(csvfile_stat, fieldnames=fieldnames_stat)
  writer_stat.writeheader()

  data = calculate('rexm', repositories_count, pull_request_count, commit_count)
  merge_status_rows = data['merge_status_data']['rows_info']
  user_statistic_info = data['user_data']
  user_merge_status_info = data['merge_status_data']['merge_statistics']
  # write merge_status_rows
  try:
    writer_merge_info.writerows(merge_status_rows)
  except:
    print('write rows to "GH_merge_stat.csv" error!')

  # write stat
  try:
    row = user_statistic_info
    row['success_merge_status_num'] = user_merge_status_info['success_num']
    row['fail_merge_status_num'] = user_merge_status_info['fail_num']
    writer_stat.writerow(user_statistic_info)
  except SyntaxError as error:
    print(error)
  except :
    print('write row to "GH_stat" error!')
  
  # path = '../GitHubLogins.txt'
  # newFile = open('GH_statuses.txt', 'a+')

  # TODO: save mergeStatisitcInfo and calculate another user info, concatenate this data ad write to a file2
  # TODO: add it for all githubIds
  
  # with open(path) as fp:  
  #   login = fp.readline()
  #   while login:
  #     row = calculate_row(login, repositories_count, pull_request_count, commit_count)
      
  #     if (row['status'] != None):
  #       newFile.write('{login}, {repo}, {pullRequest}, {commit}, {status} \n'.format(row))

  #     login = fp.readline()

main()

