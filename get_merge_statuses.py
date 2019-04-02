import csv
import requests
import time
import config

authorization_token = "Bearer {0}".format(config.TOKEN)
headers = {"Authorization": authorization_token}

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
{
  repositoryOwner(login: "IvanGoncharov") {
    repositories(last: 10) {
      nodes {
        name
        description,
        pullRequests (last: 2) {
          nodes {
            commits (last: 10){
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
}
"""