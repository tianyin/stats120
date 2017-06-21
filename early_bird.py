from config import config
from datetime import datetime
from datetime import timedelta, tzinfo
import gcommits
import os
import math

def __loadfile(fp): 
  with open(fp) as f:
    return f.read().splitlines()

def parsescore(fp):
  for l in  __loadfile(fp):
    if l.startswith('Autograde Score:'):
      return l.replace('Autograde Score: ', '').replace(' / 100', '')
  return None 
  
def getscore():
  sdict = {}
  rdir = config.get('general', 'repos_root') 
  for f in os.listdir(rdir):
    if f.startswith('nachos_fa16') == False:
      continue
    repop = os.path.join(rdir, f)
    scorep = os.path.join(repop, 'proj2/proj2.res.summary')
    if os.path.exists(scorep) == False:
      score = 0.0
    else:
      score = float(parsescore(scorep))
    sdict[f] = score
  return sdict

def mean(nums):
  return sum(nums) / len(nums)

def median(nums):
  snums = sorted(nums)
  index = (len(nums) - 1) / 2
  if len(nums)%2:
    return snums[index]
  else:
    return (snums[index] + snums[index + 1])/2.0

#scorell = getscore()
#print mean(scorell.values())

def __has_commits(commits, tset):
  for c in commits:
    datestr = c['date'].strftime("%Y-%m-%d")
    if datestr in tset:
      #print c
      return True
  return False 

def get_birds(start_date, intv):
  """
  select the repos that have commits during start_date and end_date
  where end_date = start_date + days
  """
  tset = set()
  date = start_date
  for i in range(intv):
    tset.add(date.strftime("%Y-%m-%d"))
    date += timedelta(days=1)
  #print tset

  birds = set()
  for repo, commits in gcommits.getcommits().iteritems():
    if __has_commits(commits, tset) == True:
      birds.add(repo)
  #print birds_score
  return birds

def __select(repos, sdict):
  sl = []
  for repo in sdict:
    if repo in repos:
      sl.append(sdict[repo])
  return sl 


start_date = datetime.strptime(config.get('time', 'proj1_due'), '%a %b %d %H:%M:%S %Y')
start_date += timedelta(days=1)
start_date += timedelta(days=1)
due_date = datetime.strptime(config.get('time', 'proj2_due'), '%a %b %d %H:%M:%S %Y')
print 'time diff: ', (due_date - start_date).days

sdict = getscore()
#print len(sdict), mean(sdict.values())

al = get_birds(start_date, 30)
print len(al), mean(__select(al, sdict)), median(__select(al, sdict))

intv_len = 2
intv_cnt = int(math.ceil(1.0 * (due_date - start_date).days / intv_len))

checksum = 0
overall = set()
for i in range(intv_cnt + 1):
  bs = get_birds(start_date, intv_len*i)
  bs -= overall
  checksum += len(bs)
  if len(bs) == 0:
    print 0, 0
  else:
    print len(bs), mean(__select(bs, sdict)), median(__select(bs, sdict))
  overall |= bs

print len(overall), '<>', checksum
#print len(get_birds(start_date, 10))
#print len(get_birds(start_date, 15))
#print len(get_birds(start_date, 25))
#print len(get_birds(start_date, 30))
