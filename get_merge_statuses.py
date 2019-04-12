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

def get_query(login, repositories_count, pull_rquest_count, commit_count):
  query = '''
			query($login: String!, $repositories_count: Int!, $pull_rquest_count: Int!, $commit_count: Int!) { 
				repositoryOwner(login: $login) {
          repositories(last: $repositories_count) {
            nodes {
              name
              description,
              pullRequests (last: $pull_rquest_count) {
                nodes {
                  url
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
    'pull_rquest_count': pull_rquest_count,
    'commit_count': commit_count
  }

  return query, variables

def calculate_row(login, repositories_count, pull_rquest_count, commit_count):
  query, variables = get_query(login, repositories_count, pull_rquest_count, commit_count)
  row_info = {
    'login': login,
    'repo': None,
    'pullRequest': None,
    'commit': None,
    'status': None,
  }
  result = run_query(query, variables)
  try:
    repositories = result['data']['repositoryOwner']['repositories']['nodes']
    for repository in repositories:
      row_info['repo'] = repository['name']
      pullRequests = repository['pullRequests']['nodes']
      for pullRequest in pullRequests:
        row_info['pullRequest'] = pullRequest['url'].split('/')[-1]
        commits = pullRequest['commits']['nodes']
        for commit in commits:
          row_info['commit'] = commit['commit']['commitUrl'].split('/')[-1]
          
          if (commit['commit']['status'] != None):
            row_info['status'] = commit['commit']['status']['state']
  except:
    print('Something wrong with data!')
    print(result)

  return row_info


def main():
  repositories_count = 10
  pull_rquest_count = 10
  commit_count = 10
  path = '../GitHubLogins.txt'
  newFile = open('GH_statuses.txt', 'a+')
  with open(path) as fp:  
        login = fp.readline()
        while login:
          row = calculate_row(login, repositories_count, pull_rquest_count, commit_count)
          
          if (row['status'] != None):
            newFile.write('{login}, {repo}, {pullRequest}, {commit}, {status} \n'.format(row))

          login = fp.readline()

main()

