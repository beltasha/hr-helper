def extract_user_logins(path):
  newFile = open('GitHubLogins.txt', 'a+')
  
  fp = open(path)
  for i, line in enumerate(fp):
    if i % 2 != 0:
      print(line[1:])
      newFile.write(line[1:])
  fp.close()
            
extract_user_logins('SOidsWithGH.txt')