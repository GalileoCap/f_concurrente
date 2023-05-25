import os
import json
import subprocess
import itertools as itt
import pandas as pd
from statistics import median
from tqdm import tqdm
from time import time

import utils
from utils import log, DATADIR, BUILDDIR, SAVEDT

def calcDfAndSave(df, data, fpath):
  df = pd.concat([df, pd.DataFrame(data)])
  os.makedirs(DATADIR, exist_ok = True)
  utils.saveDf(df, fpath)
  return df

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

  fpath = os.path.join(DATADIR, name + '.pkl.bz2')
  df = utils.readDf(fpath)

  cases = list(itt.product(*ranges))[len(df):] # Don't re-run cached cases
  if len(cases) == 0:
    return df

  data = []
  tstamp = time()
  for case in tqdm(cases):
    data.append(runCase(case))

    # Save frequently to avoid losing data
    if (time() - tstamp) > SAVEDT:
      df = calcDfAndSave(df, data, fpath)
      data.clear() 
      tstamp = time()

  log('[runAllCases] DONE', name, level = 'user')
  return calcDfAndSave(df, data, fpath)
