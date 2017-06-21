from config import config
import subprocess
import os
from datetime import datetime
from datetime import timedelta, tzinfo

#PATH = '/home/cse120/snapshot.proj2/nachos_fa16_davidmrdavid_ethandbrand'
#out = subprocess.check_output(['git', '-C', PATH, 'log'])
#log = out.split('\n')

class FixedOffset(tzinfo):
  """Fixed offset in minutes: `time = utc_time + utc_offset`."""
  def __init__(self, offset):
    self.__offset = timedelta(minutes=offset)
    hours, minutes = divmod(offset, 60)
    #NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
    #  that have the opposite sign in the name;
    #  the corresponding numeric value is not used e.g., no minutes
    self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)
  def utcoffset(self, dt=None):
    return self.__offset
  def tzname(self, dt=None):
    return self.__name
  def dst(self, dt=None):
    return timedelta(0)
  def __repr__(self):
    return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)

def getcommits():
  cdict = {}
  rdir = config.get('general', 'repos_root') 
  for f in os.listdir(rdir):
    if f.startswith('nachos_fa16') == False:
      continue
    fp = os.path.join(rdir, f)
    out = subprocess.check_output(['git', '-C', fp, 'log'])
    commits = parselog(out.split('\n'))
    filterTA(commits)
    cdict[f.replace('nachos_fa16_', '')] = commits
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
  tas = ['Tianyin Xu', 'Aravind Kumar', 'danielknapp', 'dknapp@ucsd.edu']
  for commit in commits:
    for ta in tas:
      #if 'Autograder' in commit['changes']:
      #  print commit
      if ta in commit['author']:
        commits.remove(commit)

def parsetstr(date_str):
  naive_date_str, _, offset_str = date_str.rpartition(' ')
  naive_dt = datetime.strptime(naive_date_str, '%a %b %d %H:%M:%S %Y')
  return naive_dt
  #offset = int(offset_str[-4:-2])*60 + int(offset_str[-2:])
  #if offset_str[0] == "-":
  #  offset = -offset
  #dt = naive_dt.replace(tzinfo=FixedOffset(offset))
  #return dt 

def find_closest(commits, start_date):
  lastcommit = None
  for commit in commits:
    if commit['date'] <= datetime.strptime('Sat Nov 19 23:59:59 2016', '%a %b %d %H:%M:%S %Y'):
      print lastcommit
    lastcommit = commit

"""
DIR = '/home/cse120/snapshot.proj2/' 
for f in os.listdir(DIR):
  fp = os.path.join(DIR, f)
  print fp
  out = subprocess.check_output(['git', '-C', fp, 'log'])
  commits = parselog(out.split('\n'))
  #print len(commits)
  filterTA(commits)
  #print len(commits)
  print '--------------------'
  #print len(commits)
  #print commits[-1]
  #find_closest(commits, None)
"""
