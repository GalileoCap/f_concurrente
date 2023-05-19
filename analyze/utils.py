import os

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
# S: Ranges ################################################

def joinRanges(*ranges):
  for r in ranges:
    for x in r:
      yield x

def testRanges():
  log('[testRanges]', level = 'user')
  modes = ['free', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = [range(1, 3)] * 5
  rangeActions = range(1, 5)
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def smallRanges():
  log('[smallRanges]', level = 'user')
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = [range(1, 10)] * 5
  rangeActions = range(1, 10)
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def mediumRanges():
  log('[mediumRanges]', level = 'user')
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    utils.joinRanges(range(1, 10), range(10, 100, 10)),
    utils.joinRanges(range(1, 10), range(10, 100, 10)),
    utils.joinRanges(range(1, 10), range(10, 100, 10)),
    utils.joinRanges(range(1, 10), range(10, 100, 10)),
    utils.joinRanges(range(1, 10), range(10, 100, 10))
  )
  rangeActions = utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100))
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)

def fullRanges():
  log('[fullRanges]', level = 'user')
  modes = ['free', 'lazy', 'optimistic', 'fine-grained', 'monitor']
  rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost = (
    utils.joinRanges(range(1, 100), range(100, 1000, 100)),
    utils.joinRanges(range(1, 100), range(100, 1000, 100)),
    utils.joinRanges(range(1, 100), range(100, 1000, 100)),
    utils.joinRanges(range(1, 100), range(100, 1000, 100)),
    utils.joinRanges(range(1, 100), range(100, 1000, 100))
  )
  rangeActions = utils.joinRanges(range(1, 10), range(10, 100, 10), range(100, 1000, 100), range(1000, 10000, 1000))
  return (modes, rangeLogIn, rangeLogOut, rangeNewPost, rangeNextPost, rangeRemovePost, rangeActions)
