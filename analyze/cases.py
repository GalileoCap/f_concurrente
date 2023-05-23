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

def getCaseFpath(mode, logIn, logOut, newPost, nextPost, removePost, actions):
  return os.path.join(DATADIR, f'{mode}_{logIn}_{logOut}_{newPost}_{nextPost}_{removePost}_{actions}.json')

def runCase(case):

  log('[runCase] RUN', case, level = 'deepDebug')
  stdout = executeCase(*case)
  data = processCaseOutput(stdout)
  data = pd.DataFrame(data, index=[0])
  data["mode"] = case[0]

  return data

def runAllCases(ranges):
  log('[runAllCases]', level = 'user')

  os.makedirs(DATADIR, exist_ok = True)

  data = pd.DataFrame()
  cases = list(itt.product(*ranges))
  for case in tqdm(cases):
    data = pd.concat([data, runCase(case)])

  data.to_csv("data.csv", index=False)

  log('[runAllCases] DONE', level = 'user')
  return data
