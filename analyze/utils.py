OUTDIR = 'out'
DATADIR = 'data'

logMask = [
  'user',
  # 'deepUser',
  # 'debug',
  'error',
  'deepDebug',
]

def log(*args, level):
  if level in logMask:
    print(*args)

