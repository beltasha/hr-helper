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


def main():
  query, variables = get_query("domi7777", 10, 10, 10)
  
  result = run_query(query, variables)
  row_info = {
    'login': "domi7777",
    'repo': None,
    'pullRequest': None,
    'commit': None,
    'status': None,
  }
  rows = []
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
          rows.append(row_info) # change to writing into file
        else:
          print('statuse is None!')

  print(rows)

main()

