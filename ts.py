from config import config
from datetime import datetime
from datetime import timedelta, tzinfo
import gcommits

dcnt = {}
cdict = gcommits.getcommits()
for repo, commits in cdict.iteritems():
  for c in commits:
    datestr = c['date'].strftime("%Y-%m-%d")
    if datestr not in dcnt:
      dcnt[datestr] = 1
    else:
      dcnt[datestr] = dcnt[datestr] + 1
  #print len(commits)
  #print commits[-1]
  #find_closest(commits, None)

init_dt  = datetime.strptime(config.get('time', 'init_repo'), '%a %b %d %H:%M:%S %Y')
final_dt = datetime.strptime(config.get('time', 'proj3_due'), '%a %b %d %H:%M:%S %Y')
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

