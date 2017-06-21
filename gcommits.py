from config import config
import subprocess
import os
from datetime import datetime
from datetime import timedelta, tzinfo

def getcommits():
  cdict = {}
  rdir = config.get('general', 'repos_root') 
  for f in os.listdir(rdir):
    if f.startswith('nachos_fa16') == False:
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
        cha = {}
        cha['version'] = revno
        cha['changes'] = message
        cha['merge'] = merge
        cha['date'] = parsetstr(date)
        cha['author'] = author
        commits.append(cha)
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
  cha = {}
  cha['version'] = revno
  cha['changes'] = message
  cha['date'] = parsetstr(date)
  cha['merge'] = merge
  cha['author'] = author
  commits.append(cha)

  return commits


def filterTA(commits):
  res = []
  tas = ['Tianyin Xu', 'Aravind Kumar', 'danielknapp', 'dknapp@ucsd.edu', 'akumark@eng.ucsd.edu']
  for commit in commits:
    ista = False
    for ta in tas:
      #if 'Autograder' in commit['changes']:
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
  #offset = int(offset_str[-4:-2])*60 + int(offset_str[-2:])
  #if offset_str[0] == "-":
  #  offset = -offset
  #dt = naive_dt.replace(tzinfo=FixedOffset(offset))
  #return dt 
