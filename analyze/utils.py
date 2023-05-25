import os
import pandas as pd

############################################################
# S: Config ################################################

OUTDIR = os.path.join(os.getcwd(), 'out')
DATADIR = os.path.join(os.getcwd(), 'data')
BUILDDIR = os.path.join(os.getcwd(), 'build')

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
  return pd.read_pickle(fpath, compression = DFCOMPRESS)

def saveDf(df, fpath):
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
  rangeLogIn, rangeLogOut, rangeNextPost = [range(1, 3+1)] * 3
  rangeNewPost, rangeRemovePost = ([0], [0])
  rangeActions = range(1, 5+1)
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def smallRanges():
  modes = ['free', 'optimistic', 'fine-grained']
  # rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = [range(1, 10+1)] * 5
  rangeLogIn, rangeLogOut, rangeNextPost = [range(1, 10+1)] * 3
  rangeNewPost, rangeRemovePost = ([0], [0])
  rangeActions = range(1, 10+1)
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def mediumRanges():
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10)),
    joinRanges(range(1, 10), range(10, 100+1, 10))
  )
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000+1, 100))
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def fullRanges(): # TODO: Not full anymore, change to large
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100)),
    joinRanges(range(1, 100, 5), range(100, 1000+1, 100))
  )
  rangeActions = joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000+1, 1000))
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

Ranges = {
  'test': testRanges(),
  'small': smallRanges(),
  # 'medium': mediumRanges(),
  # 'full': fullRanges(),
}
