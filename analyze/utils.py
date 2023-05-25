import os
import pandas as pd

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
  rangeLogIn, rangeLogOut, rangeNextPost = [range(1, 3+1)] * 3
  rangeNewPost, rangeRemovePost = ([0], [0])
  return (modes, rangeActions, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost)

def smallRanges():
  modes = ['free', 'optimistic', 'fine-grained']
  rangeActions = range(1, 10+1)
  # rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = [range(1, 10+1)] * 5
  rangeLogIn, rangeLogOut, rangeNextPost = [range(1, 10+1)] * 3
  rangeNewPost, rangeRemovePost = ([0], [0])
  return (modes, rangeActions, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost)

def mediumRanges():
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000+1, 100))
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10))
  )
  return (modes, rangeActions, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost)

def fullRanges(): # TODO: Not full anymore, change to large
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100))
  )
  return (modes, rangeActions, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost)

Ranges = {
  'test': testRanges(),
  'small': smallRanges(),
  # 'medium': mediumRanges(),
  # 'full': fullRanges(),
}
