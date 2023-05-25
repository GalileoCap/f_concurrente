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

def filterCases(ranges, df):
  cached = set(df[['mode', 'actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads', 'repeat']].itertuples(index = False, name = None)) if len(df) > 0 else set()
  for case in itt.product(*ranges):
    if case not in cached:
      yield case
    else:
      cached.remove(case)

def executeCase(mode, actions, logIn, logOut, apiRequest, _):
  cmd = f'java -cp {BUILDDIR} ThreadPool {mode} {actions} {logIn} {logOut} {apiRequest}'
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
  data['actions'] = case[1]
  data['logIn_threads'] = case[2]
  data['logOut_threads'] = case[3]
  data['apiRequest_threads'] = case[4]
  data['repeat'] = case[5]

  return data

def runAllCases(name, ranges):
  ranges, total = ranges
  log('[runAllCases]', name, level = 'user')

  fpath = os.path.join(DATADIR, name + '.pkl.bz2')
  df = utils.readDf(fpath) # Try to read cached cases

  data = []
  tstamp = time()
  for case in tqdm(filterCases(ranges, df), initial = len(df), total = total): #NOTE: Skips cached cases
    data.append(runCase(case))

    # Save frequently to avoid losing data
    if (time() - tstamp) > SAVEDT:
      df = calcDfAndSave(df, data, fpath)
      data.clear() 
      tstamp = time()

  log('[runAllCases] DONE', name, level = 'user')
  return calcDfAndSave(df, data, fpath)
