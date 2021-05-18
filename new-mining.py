import os
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests
import json

def readInputJson():
  # Opening JSON file
  f = open('config.json',)
  # returns JSON object as a dictionary
  config = json.load(f)
  return config

def getFilenameGist(config):
  if ('filenameGist' not in config):
    return None
  else:
    return config['filenameGist']

def getFilenameUser(config):
  if ('filenameUsers' not in config):
    return None
  else:
    return config['filenameUsers']

def getToken(config):
  if ('github_token' not in config):
    return None
  else:
    list_tokens = []
    for token in config['github_token']:
      list_tokens.append(token)
    return list_tokens

def getUsers(config):
  if ('users_list' not in config):
    return None
  else:
    list_users = []
    for user in config['users_list']:
      list_users.append(user)
    return list_users

def getUserInfo(url, headers):
  r = requests.get(url, headers=headers)
  json_info_user = r.json()
  return json_info_user

def getGists(url, headers, nGist):
  json_gists = []
  for x in range(0, nGist, 100):
    params = {
      "per_page": "100",
      "page": x
    }
    r = requests.get(url, headers=headers, params=params)
    json_gists.append(r.json())
  return json_gists

def getGistsInfo(url, headers):
  r = requests.get(url, headers=headers)
  json_gist_info = r.json()
  return json_gist_info

if __name__ == '__main__':
  config = readInputJson()
  tokens = getToken(config)
  filenameGist = getFilenameGist(config)
  filenameUser = getFilenameUser(config)
  if (tokens == None):
    print('Error: Token not found!')
  else:
    headers = {
      'Authorization': f'token {tokens[0]}',
      'Accept': f'application/vnd.github.v3+json'
    }
    users = getUsers(config)
    list_info = []
    list_gists_info = []
    control = False
    controlUser = False
    for user in users:
      list_info = []
      list_gists_url = []
      url = f"https://api.github.com/users/" + user
      info = getUserInfo(url, headers)
      if (info != {}):
        if ('gists_url' not in info):
          print('Error: Not found GISTS_URL!')
          pass
        else:
          gists_url = info['gists_url'].split("{")[0]
          nGist = info['public_gists']
          gists_list = getGists(gists_url, headers, nGist)
          if (len(gists_list) > 0):
            list_gists_url = [gist['url'] for gist in gists_list[0] if 'url' in gist]
          for url_gist in list_gists_url:
            list_gists_info = []
            gist_info = getGistsInfo(url_gist, headers)
            if ('files' in gist_info):
              info_norm = info
              gist_info_norm = gist_info

              gist_info_norm['gist_id'] = gist_info_norm['id']
              gist_info_norm['gist_created_at'] = pd.to_datetime(gist_info_norm['created_at']).date()

              gist_info_norm['gist_updated_at'] = pd.to_datetime(gist_info_norm['updated_at']).date()

              gist_info_norm['files_key'] = list(gist_info_norm['files'])

              gist_info_norm['language'] = [i['language'] for file, i in gist_info_norm['files'].items() if i['language'] != None]
              gist_info_norm['type'] = [i['type'] for file, i in gist_info_norm['files'].items() if i['type'] != None]
              gist_info_norm['size'] = [i['size'] for file, i in gist_info_norm['files'].items()]
              gist_info_norm['totalSize'] = sum(gist_info_norm['size'])

              gist_info_norm['total'] = 0
              gist_info_norm['additions'] = 0
              gist_info_norm['deletions'] = 0
              gist_info_norm['changes'] = 0
              if ('history' in gist_info):
                for history in gist_info_norm['history']:
                  if (history['change_status'] != {}):
                    gist_info_norm['changes'] += 1
                    gist_info_norm['total'] += history['change_status']['total']
                    gist_info_norm['additions'] += history['change_status']['additions']
                    gist_info_norm['deletions'] += history['change_status']['deletions']
                
              gist_info_norm['number_files'] = len(list(gist_info_norm['files']))
              gist_info_norm['number_forks'] = len(list(gist_info_norm['forks']))
              if (len(list(gist_info_norm['forks'])) > 0):
                gist_info_norm['has_forks'] = 'TRUE'
              else:
                gist_info_norm['has_forks'] = 'FALSE'
              list_gists_info.append([
                info_norm['login'],
                gist_info_norm['gist_id'],
                gist_info_norm['html_url'],
                gist_info_norm['files_key'],
                gist_info_norm['number_files'],
                gist_info_norm['language'],
                gist_info_norm['type'],
                gist_info_norm['size'],
                gist_info_norm['totalSize'],
                gist_info_norm['files'],
                gist_info_norm['gist_created_at'],
                gist_info_norm['gist_updated_at'],
                gist_info_norm['description'],
                gist_info_norm['comments'],
                gist_info_norm['has_forks'],
                gist_info_norm['number_forks'],
                gist_info_norm['forks'],
                gist_info_norm['history'],
                gist_info_norm['total'],
                gist_info_norm['additions'],
                gist_info_norm['deletions'],
                gist_info_norm['changes'],
              ])
              dataset = pd.DataFrame(list_gists_info)
              dataset.columns = [
                'login',
                'gist_id',
                'html_url',
                'files_key',
                'files_number',
                'files_language',
                'files_type',
                'files_size',
                'files_total_size',
                'files',
                'gist_created_at',
                'gist_updated_at',
                'description',
                'comments',
                'forks_has',
                'forks_number',
                'forks',
                'history',
                'history_total',
                'history_additions',
                'history_deletions',
                'history_changes',
              ]
              if (control == False):
                dataset.to_csv(filenameGist, index=False, header=True, mode='a')
                control = True
              else:
                dataset.to_csv(filenameGist, index=False, header=False, mode='a')
        info_norm = info
        info_norm['acc_created_at'] = pd.to_datetime(info_norm['created_at']).date()
        info_norm['acc_updated_at'] = pd.to_datetime(info_norm['updated_at']).date()
        if (info_norm['hireable'] == True):
          info_norm['hireable'] = 'TRUE'
        else:
          info_norm['hireable'] = 'FALSE'
        list_info.append([
          info_norm['login'],
          info_norm['name'],
          info_norm['email'],
          info_norm['html_url'],
          info_norm['acc_created_at'],
          info_norm['acc_updated_at'],
          info_norm['followers'],
          info_norm['following'],
          info_norm['location'],
          info_norm['hireable'],
          info_norm['company'],
          info_norm['blog'],
          info_norm['public_gists'],
          info_norm['public_repos'],
          info_norm['type'],
        ])
        datasetUser = pd.DataFrame(list_info)
        datasetUser.columns = [
          'login',
          'name',
          'email',
          'html_url',
          'acc_created_at',
          'acc_updated_at',
          'followers',
          'following',
          'location',
          'hireable',
          'company',
          'blog',
          'public_gists',
          'public_repos',
          'type',
        ]
        if (controlUser == False):
          datasetUser.to_csv(filenameUser, index=False, header=True, mode='a')
          controlUser = True
        else:
          datasetUser.to_csv(filenameUser, index=False, header=False, mode='a')


      
    