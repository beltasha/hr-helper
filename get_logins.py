import csv
import requests
import time
import config

authorization_token = "Bearer {0}".format(config.TOKEN)
headers = {"Authorization": authorization_token}

def get_user_by_id(param):
    url = 'https://api.github.com/user/' + str(param)
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed to run by returning code of {}. {}'.format(request.status_code, url))

def extract_user_ids(path):
    newFile = open('GH_ids.txt', 'a+')
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            newFile.write('%s\n' % row[0])
        
def prepare_user_logins(path):
    newFile = open('GH_logins.txt', 'a+')
    with open(path) as fp:  
        id = fp.readline()
        while id:
            write_user_login(int(id), newFile)
            id = fp.readline()

def write_user_login(id, newFile):
  try:
    user = get_user_by_id(id)
    newFile.write('%s\n' % user['login'])
    print('User with id {0} has login {1}'.format(id, user['login']))
  except:
    print('User with id {0} not found!'.format(id))
  time.sleep(2)

# extract ids from 'dataset.csv' to a new file
extract_user_ids('dataset.csv')

# get user login by id and write to a new file
prepare_user_logins('GH_ids.txt')