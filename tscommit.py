from config import config
from datetime import datetime
from datetime import timedelta, tzinfo
import gcommits
import os
import subprocess
#print config.get('default', 'init_push')

dcnt = {}

DIR = '/home/cse120/snapshot.proj2/' 
for f in os.listdir(DIR):
  fp = os.path.join(DIR, f)
  #print fp
  out = subprocess.check_output(['git', '-C', fp, 'log'])
  commits = gcommits.parselog(out.split('\n'))
  gcommits.filterTA(commits)
  for c in commits:
    datestr = c['date'].strftime("%Y-%m-%d")
    if datestr not in dcnt:
      dcnt[datestr] = 1
    else:
      dcnt[datestr] = dcnt[datestr] + 1
  #print len(commits)
  #print commits[-1]
  #find_closest(commits, None)

init_dt  = datetime.strptime(config.get('default', 'init_repo'), '%a %b %d %H:%M:%S %Y')
final_dt = datetime.strptime(config.get('default', 'proj3_due'), '%a %b %d %H:%M:%S %Y')
#print type(final_dt - init_dt)
qdays = (final_dt - init_dt).days

date = init_dt
for i in range(qdays + 1): 
    dtstr = date.strftime("%Y-%m-%d")
    if dtstr in dcnt:
      print dtstr + '\t' + str(dcnt[dtstr])
    else:
      print dtstr + '\t' + str(0)
    date += timedelta(days=1)

