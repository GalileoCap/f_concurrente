import os
import json
import subprocess
import itertools as itt

import utils
from utils import log

def executeCase(mode, logIn, logOut, newPost, nextPost, removePost, actions):
  cmd = f'java -cp ../build ThreadPool {mode} {logIn} {logOut} {newPost} {nextPost} {removePost} {actions}'
  res = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE)
  res.check_returncode()
  return res.stdout

def processCaseOutput(stdout):
  # Read its output
  data = dict()
  lines = stdout.decode('utf-8').split('\n')[:-1] # Last one is empty
  for out in (line.split(', ') for line in lines):
    mode = out[0]
    times = [int(t) for t in out[1:]]
    data[mode] = data.get(mode, []) + times
  return data

def getCaseFpath(mode, logIn, logOut, newPost, nextPost, removePost, actions):
  return f'../data/{mode}_{logIn}_{logOut}_{newPost}_{nextPost}_{removePost}_{actions}.json'

def runCase(case, force = False):
  fpath = getCaseFpath(*case)

  # If this case has already been executed and saved, load it
  if not force and os.path.isfile(fpath):
    log('[runCase] LOAD', case, level = 'deepDebug')
    with open(fpath, 'r') as fin:
      return json.load(fin)

  log('[runCase] RUN', case, level = 'deepDebug')
  stdout = executeCase(*case)
  data = processCaseOutput(stdout)

  # Save it
  with open(fpath, 'w') as fout:
    fout.write(json.dumps(data))

  return data

def runAllCases(ranges, force = False):
  log('[runAllCases]', level = 'user')
  for case in itt.product(*ranges):
    runCase(case, force)

if __name__ == '__main__':
  os.makedirs('../data', exist_ok = True)
  
  modes = ['monitor', 'free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  maxThreads = 1
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100)),
    utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100)),
    utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100)),
    utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100)),
    utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100))
  )
  rangeActions = utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100))
  runAllCases((modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions))

