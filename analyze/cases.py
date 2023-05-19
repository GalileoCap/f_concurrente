import os
import json
import subprocess
import itertools as itt

import utils
from utils import log, DATADIR, BUILDDIR

def executeCase(mode, logIn, logOut, newPost, nextPost, removePost, actions):
  cmd = f'java -cp {BUILDDIR} ThreadPool {mode} {logIn} {logOut} {newPost} {nextPost} {removePost} {actions}'
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
  return os.path.join(DATADIR, f'{mode}_{logIn}_{logOut}_{newPost}_{nextPost}_{removePost}_{actions}.json')

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

  os.makedirs(DATADIR, exist_ok = True)

  data = dict()
  for case in itt.product(*ranges):
    data[case] = runCase(case, force)

  log('[runAllCases] DONE', level = 'user')
  return data
