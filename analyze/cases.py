import os
import json
import subprocess
import itertools as itt
import pandas as pd

import utils
from utils import log, DATADIR, BUILDDIR
from statistics import median
from tqdm import tqdm

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
  for mode, times in data.items():
    data[mode] = median(times)
  return data

def runCase(case):
  log('[runCase] RUN', case, level = 'deepDebug')

  stdout = executeCase(*case)
  data = processCaseOutput(stdout)
  data['mode'] = case[0]

  return data

def runAllCases(name, ranges):
  log('[runAllCases]', name, level = 'user')

  fpath = os.path.join(DATADIR, name + '.csv')
  if os.path.isfile(fpath):
    log('[runAllCases] LOAD', name, level = 'debug')
    return pd.read_csv(fpath)

  data = []
  for case in tqdm(list(itt.product(*ranges))):
    data.append(runCase(case))
  df = pd.DataFrame(data)

  os.makedirs(DATADIR, exist_ok = True)
  df.to_csv(fpath, index = False)

  log('[runAllCases] DONE', name, level = 'user')
  return df
