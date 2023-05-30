import os
import json
import subprocess
import pandas as pd
from statistics import median, mean, stdev
from tqdm import tqdm
from time import time

import utils
from utils import log, DATADIR, BUILDDIR, SAVEDT

def calcDfAndSave(df, data, fpath):
  df = pd.concat([df, pd.DataFrame(data)])
  os.makedirs(DATADIR, exist_ok = True)
  utils.saveDf(df, fpath)
  return df

def filterCases(cases, df):
  # TODO: Fix case2 not filtering correctly
  for i, case in enumerate(cases):
    if i < len(df):
      continue
    yield case
  # cached = set(df[['mode', 'actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads', 'repeat']].itertuples(index = False, name = None)) if len(df) > 0 else set()
  # for case in cases:
    # if case not in cached:
      # yield case
    # else:
      # cached.remove(case)

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
  
  res = dict()
  totalTime = 0
  for mode, times in data.items():
    res[f'{mode}_medianTime'] = median(times)
    res[f'{mode}_meanTime'] = mean(times)
    res[f'{mode}_stdTime'] = stdev(times) if len(times) > 1 else 0
    totalTime += sum(times)

  res['totalTime'] = totalTime

  return res

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

def runAllCases(name, cases):
  cases, total = cases
  log('[runAllCases]', name, level = 'user')

  fpath = utils.dfPath(name)
  df = utils.readDf(fpath) # Try to read cached cases

  data = []
  tstamp = time()
  for case in tqdm(filterCases(cases, df), initial = len(df), total = total): #NOTE: Skips cached cases
    try:
      data.append(runCase(case))

      # Save frequently to avoid losing data
      if (time() - tstamp) > SAVEDT:
        df = calcDfAndSave(df, data, fpath)
        data.clear() 
        tstamp = time()
    except Exception as err:
      log('Error with case', case, err, level = 'error')

  log('[runAllCases] DONE', name, level = 'user')
  return calcDfAndSave(df, data, fpath)
