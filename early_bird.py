from config import config
from datetime import datetime
from datetime import timedelta, tzinfo
import commit_parser
import os
import math

def __loadfile(fp): 
  with open(fp) as f:
    return f.read().splitlines()

def __mean(nums):
  return sum(nums) / len(nums)

def __median(nums):
  snums = sorted(nums)
  index = (len(nums) - 1) / 2
  if len(nums)%2:
    return snums[index]
  else:
    return (snums[index] + snums[index + 1])/2.0

def parsescore(fp):
  for l in  __loadfile(fp):
    if l.startswith('Autograde Score:'):
      return l.replace('Autograde Score: ', '').replace(' / 100', '')
  return None 
  
def getscore(proj):
  sdict = {}
  rdir = config.get('general', 'repos_root') 
  for f in os.listdir(rdir):
    if f.startswith(config.get('general', 'repo_prefix')) == False:
      continue
    repop = os.path.join(rdir, f)
    scorep = os.path.join(repop, config.get(proj, 'proj_score'))
    if os.path.exists(scorep):
      score = float(parsescore(scorep))
    else:
      score = 0.0
    sdict[f] = score
  return sdict

#scorell = getscore()
#print __mean(scorell.values())

def __has_commits(commits, dt_set):
  for c in commits:
    datestr = c['date'].strftime("%Y-%m-%d")
    if datestr in dt_set:
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
  for repo, commits in commit_parser.getcommits().iteritems():
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


def runbirds(projx, intv_len=2): 
  start_date = datetime.strptime(config.get(projx, 'proj_start'), '%a %b %d %H:%M:%S %Y')
  start_date += timedelta(days=1)
  start_date += timedelta(days=1)
  due_date = datetime.strptime(config.get(projx, 'proj_due'), '%a %b %d %H:%M:%S %Y')
  dspan = (due_date - start_date).days
  print projx, ' takes ', dspan, 'days'

  sdict = getscore(projx)
  #print len(sdict), __mean(sdict.values())

  al = get_birds(start_date, dspan)
  print '-----------------------'
  print 'intv #repo mean median'
  print '-----------------------'
  print 'all', len(al), __mean(__select(al, sdict)), __median(__select(al, sdict))
  print '-----------------------'
  intv_cnt = int(math.ceil(1.0 * dspan / intv_len))

  overall = set()
  for i in range(intv_cnt + 1):
    bs = get_birds(start_date, intv_len*i)
    bs -= overall
    if len(bs) == 0:
      print 0, 0
    else:
      print str(intv_len*(i-1))+'-'+str(intv_len*i), len(bs), __mean(__select(bs, sdict)), __median(__select(bs, sdict))
    overall |= bs  

if __name__ == "__main__":
  print '-----------------------'
  runbirds('proj2')
  print '-----------------------'
  runbirds('proj3')
#print len(get_birds(start_date, 10))
#print len(get_birds(start_date, 15))
#print len(get_birds(start_date, 25))
#print len(get_birds(start_date, 30))
