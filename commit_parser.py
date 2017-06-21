from config import config
import subprocess
import os
from datetime import datetime
from datetime import timedelta, tzinfo

def getcommits():
  cdict = {}
  rdir = config.get('general', 'repos_root') 
  for f in os.listdir(rdir):
    if f.startswith(config.get('general', 'repo_prefix')) == False:
      continue
    fp = os.path.join(rdir, f)
    out = subprocess.check_output(['git', '-C', fp, 'log'])
    commits = parselog(out.split('\n'))
    cdict[f] = filterTA(commits)
  return cdict

def parselog(log):
  commits = []
  
  revno = None
  message = ''
  author = None
  date = None
  merge = None
  for line in log:
    if len(line.strip()) == 0:
      continue
    if line.startswith('commit '):
      if revno != None:
        com = {}
        com['version'] = revno
        com['message'] = message
        com['merge'] = merge
        com['date'] = parsetstr(date)
        com['author'] = author
        commits.append(com)
      revno = line.replace('commit', '').strip()
      message = ''
      date = None
      merge = None
      chfiles = []
    elif line.startswith('Author:'):
      author = line.replace('Author:', '').strip()
    elif line.startswith('Merge:'):
      merge = line.replace('Merge:', '').strip()
    elif line.startswith('Date:'):
      date = line.replace('Date:', '').strip()
    elif line.startswith('    '):
      message += line.strip() + ' '
    else:
      print 'ERROR:', line

  # the last commit
  com = {}
  com['version'] = revno
  com['message'] = message
  com['date'] = parsetstr(date)
  com['merge'] = merge
  com['author'] = author
  commits.append(com)

  return commits


def filterTA(commits):
  res = []
  tas = config.get('general', 'ta_list').split(',')
  for commit in commits:
    ista = False
    for ta in tas:
      #if 'Autograder' in commit['comnges']:
      #  print commit
      if ta in commit['author']:
        ista = True
        break
    if ista == False:
      res.append(commit)
  return res

def parsetstr(date_str):
  naive_date_str, _, offset_str = date_str.rpartition(' ')
  naive_dt = datetime.strptime(naive_date_str, '%a %b %d %H:%M:%S %Y')
  return naive_dt
