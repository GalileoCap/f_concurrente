import os
import pandas as pd
import itertools as itt

############################################################
# S: Config ################################################

OUTDIR = os.path.join(os.getcwd(), 'out')
DATADIR = os.path.join(os.getcwd(), 'data')
BUILDDIR = os.path.join(os.getcwd(), 'build')

SAVEDT = 5 * 60 # In seconds

MODES = ['free', 'optimistic', 'fine-grained']
# MODES = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']

############################################################
# S: Log ###################################################

logMask = [
  'user',
  # 'deepUser',
  # 'debug',
  'error',
  # 'deepDebug',
]

def log(*args, level):
  if level in logMask:
    print(*args)

############################################################
# S: Df Management #########################################

DFCOMPRESS = 'bz2'

def readDf(fpath):
  print(fpath)
  if os.path.isfile(fpath):
    log('[readDf] LOAD', fpath, level = 'debug')
    return pd.read_pickle(fpath, compression = DFCOMPRESS)
  else:
    log('[readDf] NOT FOUND', fpath, level = 'debug')
    return pd.DataFrame()

def saveDf(df, fpath):
  log('[saveDf]', fpath, level = 'deepDebug')
  return df.to_pickle(fpath, compression = DFCOMPRESS)

def dfPkl2Csv(ipath, opath):
  df = readDf(ipath)
  df.to_csv(opath, index = False)

def dfCsv2Pkl(ipath, opath):
  df = pd.read_csv(ipath)
  saveDf(df, opath)

############################################################
# S: Cases #################################################

def joinCases(*ranges):
  for r in ranges:
    for x in r:
      yield x

def testCases():
  modes = ['free', 'monitor']
  rangeActions = range(1, 5+1)
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 3+1)] * 3
  repeat = range(3)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 2 * 5 * 3**3 * 3)

def ACases(): # TODO: Rename
  modes = MODES

  totalThreads = 100
  threadsRange = range(1, totalThreads+1, 1)

  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, thisThreads, actions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      othersThreads = (totalThreads - thisThreads) // 2
      thisThreads += (totalThreads - thisThreads) % 2 # Fix rounding errors

      yield (mode, actions, thisThreads, othersThreads, othersThreads, r) # logIn
      yield (mode, actions, othersThreads, thisThreads, othersThreads, r) # logOut
      yield (mode, actions, othersThreads, othersThreads, thisThreads, r) # apiRequest

  return (iterate(), 3 * len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

def BCases(): # TODO: Rename
  modes = MODES
  threadsRange = range(3, 150+1, 3)
  actionsRange = [300]
  repeatRange = range(10)

  def iterate():
    for mode, totalThreads, totalActions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      threads = totalThreads // 3
      actions = actionsRange // threads

      yield (mode, actions, threads, threads, threads, r)

  return (iterate(), 3 * len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

def CCases(): # TODO: Rename
  modes = MODES
  threadsRange = range(3, 150+1, 3)
  actionsRange = [10]
  repeatRange = range(10)

  def iterate():
    for mode, totalThreads, actions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      threads = totalThreads // 3

      yield (mode, actions, threads, threads, threads, r)

  return (iterate(), 3 * len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

def singleCases(): # TODO: Rename
  modes = MODES
  threadsRange = range(1, 150+1, 1)
  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, threads, actions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      yield (mode, actions, threads, 0, 0, r) # logIn
      yield (mode, actions, 0, threads, 0, r) # logOut
      yield (mode, actions, 0, 0, threads, r) # apiRequest

  return (iterate(), 3 * len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

def doubleCases(): # TODO: Rename
  modes = MODES
  threadsRange = range(2, 150+1, 2)
  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, threads, actions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      threads = threads // 2
      yield (mode, actions, threads, threads, 0, r) # logIn & logOut
      yield (mode, actions, threads, 0, threads, r) # logIn & apiRequest
      yield (mode, actions, 0, threads, threads, r) # logOut & apiRequest

  return (iterate(), 3 * len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

def tripleCases(): # TODO: Rename
  modes = MODES
  threadsRange = range(3, 150+1, 3)
  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, threads, actions, r in itt.product(modes, threadsRange, actionsRange, repeatRange):
      threads = threads // 3
      yield (mode, actions, threads, threads, threads, r)

  return (iterate(), len(modes) * len(threadsRange) * len(actionsRange) * len(repeatRange))

Ranges = {
  'test': testCases(),
  
  'A': ACases(),
  'B': BCases(),
  'C': CCases(),

  'single': singleCases(),
  'double': doubleCases(),
  'triple': tripleCases(),
}

############################################################
# S: Misc ##################################################

def htmlPath(fbase, name):
  fbase = os.path.join(OUTDIR, fbase)
  os.makedirs(fbase, exist_ok = True)
  return os.path.join(fbase, f'{name}.html')

def imgPath(fbase, name):
  fbase = os.path.join(OUTDIR, fbase)
  os.makedirs(fbase, exist_ok = True)
  return os.path.join(fbase, f'{name}.pdf')

def dfPath(name):
  return os.path.join(DATADIR, name + '.pkl.bz2')
