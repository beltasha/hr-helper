import csv
import requests
import time
import config

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
  query, variables = get_query("domi7777", 10, 5, 10)
  statuses = run_query(query, variables)
  print(statuses)

main()

