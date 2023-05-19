OUTDIR = 'out'
DATADIR = 'data'

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

def joinRanges(*ranges):
  for r in ranges:
    for x in r:
      yield x
