from config import config
from datetime import datetime
from datetime import timedelta, tzinfo
import gcommits
import os

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

start_date = datetime.strptime(config.get('time', 'proj1_due'), '%a %b %d %H:%M:%S %Y')
start_date += timedelta(days=1)
start_date += timedelta(days=1)


def select(repos, sdict):
  sl = []
  for repo in sdict:
    if repo in repos:
      sl.append(sdict[repo])
  return sl 

sdict = getscore()
print len(sdict), mean(sdict.values())

al = get_birds(start_date, 30)
print len(al), mean(select(al, sdict)), median(select(al, sdict))

checksum = 0
overall = set()
for i in range(15):
  bs = get_birds(start_date, 2*i)
  bs -= overall
  checksum += len(bs)
  if len(bs) == 0:
    print 0, 0
  else:
    print len(bs), mean(select(bs, sdict)), median(select(bs, sdict))
  overall |= bs

print len(overall), '<>', checksum
#print len(get_birds(start_date, 10))
#print len(get_birds(start_date, 15))
#print len(get_birds(start_date, 25))
#print len(get_birds(start_date, 30))
