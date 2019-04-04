import csv
import requests
import time
import config

authorization_token = "Bearer {0}".format(config.TOKEN)
headers = {"Authorization": authorization_token}

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def get_query(login, repositories_count, pull_rquest_count, commit_count):
  return """ {
    repositoryOwner(login: {0}) {
      repositories(last: {1}) {
        nodes {
          name
          description,
          pullRequests (last: {2}) {
            nodes {
              commits (last: {3}){
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
  } """.format(login, repositories_count, pull_rquest_count, commit_count)

