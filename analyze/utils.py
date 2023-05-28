import os
import pandas as pd
import itertools as itt

############################################################
# S: Config ################################################

OUTDIR = os.path.join(os.getcwd(), 'out')
DATADIR = os.path.join(os.getcwd(), 'data')
BUILDDIR = os.path.join(os.getcwd(), 'build')

SAVEDT = 5 * 60 # In seconds

MODES = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor', 'un']

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
  # modes = ['free', 'monitor', 'un']
  modes = MODES
  rangeActions = range(1, 5+1)
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 3+1)] * 3
  repeat = range(3)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), len(modes) * 5 * 3**3 * 3)

def smallRanges():
  modes = ['free', 'optimistic', 'fine-grained']
  rangeActions = range(1, 10+1)
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 10+1)] * 3
  repeat = range(5)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 3 * 10 * 10**3 * 5)

def mediumRanges():
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000+1, 100))
  rangeLogIn, rangeLogOut, rangeApiRequest = (
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10))
  )
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (3 * 10) * (2 * 10)**3 * 10)

def largeRanges():
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  rangeLogIn, rangeLogOut, rangeApiRequest = (
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
  )
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (4 * 10) * (20 + 10)**3 * 10)

def fullRanges():
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  rangeLogIn, rangeLogOut, rangeApiRequest = [range(1, 1000)] * 3
  repeat = range(10)
  return (itt.product(modes, rangeActions, rangeLogIn, rangeLogOut, rangeApiRequest, repeat), 5 * (4 * 10) * 1000**3 * 10)

def case1Ranges(): # TODO: Rename
  modes = MODES
  rangeTotalThreads = [(100, 1), (1000, 100)]
  rangeActions = joinRanges(range(10, 100+1, 10), range(100, 1000+1, 100))
  repeat = range(10)

  def iterate():
    for mode, (totalThreads, step), actions, r in itt.product(modes, rangeTotalThreads, rangeActions, repeat):
      for thisThreads in range(0, totalThreads+1, step):
        othersThreads = (totalThreads - thisThreads) // 2 
        thisThreads += (totalThreads - thisThreads) % 2 # +1 to fix rounding errors

        yield (mode, actions, thisThreads, othersThreads, othersThreads, r) # logIn
        yield (mode, actions, othersThreads, thisThreads, othersThreads, r) # logOut
        yield (mode, actions, othersThreads, othersThreads, thisThreads, r) # apiRequest

  return (iterate(), 3 * len(modes) * (100 + 10) * 20 * len(repeat)) # TODO: Calculate length

def case2Ranges(): # TODO: Rename
  modes = MODES 
  rangeActions = range(3, 150, 3) # Will usually be split by three types of actions
  repeat = 5

  def cases():
    for totalActions in rangeActions:
      max_threads = totalActions // 3  # More threads not needed
      rangeThreads = range(1, max_threads+1)
      for threads in rangeThreads:
        actions = max(totalActions // (3 * threads), 1)
        for mode, r in itt.product(modes, range(repeat)):
          yield (mode, actions, threads, threads, threads, r)

  return (cases(), 30625) # Not sure how to calculate the total cases programmatically


Ranges = {
  'case1': case1Ranges(),
  'case2': case2Ranges(),

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
  return os.path.join(fbase, f'{name}.png')
