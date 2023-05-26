import os
import pandas as pd
import itertools as itt

############################################################
# S: Config ################################################

OUTDIR = os.path.join(os.getcwd(), 'out')
DATADIR = os.path.join(os.getcwd(), 'data')
BUILDDIR = os.path.join(os.getcwd(), 'build')

SAVEDT = 5 * 60 # In seconds

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

Ranges = {
  'test': testRanges(),
  'small': smallRanges(),
  'medium': mediumRanges(),
  'large': largeRanges(),
  'full': fullRanges(),
}
