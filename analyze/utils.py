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
# S: Ranges ################################################

def joinRanges(*ranges):
  for r in ranges:
    for x in r:
      yield x

def testRanges():
  modes = ['free', 'monitor']
  rangeActions = range(1, 5+1)
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 3+1)] * 3
  repeat = range(3)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 2 * 5 * 3**3 * 3)

def smallRanges():
  modes = MODES
  rangeActions = range(1, 10+1)
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 10+1)] * 3
  repeat = range(5)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 3 * 10 * 10**3 * 5)

def mediumRanges():
  modes = MODES
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000+1, 100))
  rangeLogIn, rangeLogOut, rangeApiRequest = (
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10))
  )
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (3 * 10) * (2 * 10)**3 * 10)

def largeRanges():
  modes = MODES
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  rangeLogIn, rangeLogOut, rangeApiRequest = (
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
  )
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (4 * 10) * (20 + 10)**3 * 10)

def fullRanges():
  modes = MODES
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 1000)] * 3
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (4 * 10) * 1000**3 * 10)

def case1Ranges(): # TODO: Rename
  modes = MODES
  totalThreads, totalThreadsStep = 100, 1
  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, thisThreads, actions, r in itt.product(modes, range(1, totalThreads+1, totalThreadsStep), actionsRange, repeatRange):
      othersThreads = (totalThreads - thisThreads) // 2 
      thisThreads += (totalThreads - thisThreads) % 2 # +1 to fix rounding errors

      yield (mode, actions, thisThreads, othersThreads, othersThreads, r) # logIn
      yield (mode, actions, othersThreads, thisThreads, othersThreads, r) # logOut
      yield (mode, actions, othersThreads, othersThreads, thisThreads, r) # apiRequest

  return (iterate(), 3 * len(modes) * (totalThreads / totalThreadsStep) * len(actionsRange) * len(repeatRange))

def case2Ranges(): # TODO: Rename
  modes = MODES
  totalThreadsRange = range(1, 150+1, 3)
  actionsRange = range(10, 100+1, 10)
  repeatRange = range(10)

  def iterate():
    for mode, totalThreads, actions, r in itt.product(modes, totalThreadsRange, actionsRange, repeatRange):
      eachThreads = totalThreads // 3

      yield (mode, actions, eachThreads, eachThreads, eachThreads, r)

  return (iterate(), len(modes) * len(totalThreadsRange) * len(actionsRange) * len(repeatRange))

def case3Ranges(): # TODO: Rename
  modes = MODES
  totalThreadsRange = range(1, 300+1, 3)
  totalActionsRange = [3 * 100]
  repeatRange = range(10)

  def iterate():
    for mode, totalThreads, totalActions, r in itt.product(modes, totalThreadsRange, totalActionsRange, repeatRange):
      actions = totalActions // 3
      eachThreads = totalThreads // 3

      yield (mode, actions, eachThreads, eachThreads, eachThreads, r)

  return (iterate(), len(modes) * len(totalThreadsRange) * len(totalActionsRange) * len(repeatRange))

Ranges = {
  'case1': case1Ranges(),
  'case2': case2Ranges(),
  'case3': case3Ranges(),

  'test': testRanges(),
  'small': smallRanges(),
  'medium': mediumRanges(),
  'large': largeRanges(),
  'full': fullRanges(),
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
