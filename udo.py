############################################################
# S: Utils #################################################

UDOConfig = {
  'version': (1, 3, 0)
}

from pathlib import Path

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

def rangesAction(ranges):
  return f'PIPENV_PIPFILE=./analyze/Pipfile pipenv run python ./analyze/main.py {ranges}'

def copyPrevAction(prev, curr):
  opath = f'./data/{curr}.pkl.bz2'
  return f'[ ! -f {opath} ] && cp ./data/{prev}.pkl.bz2 {opath} || :'

############################################################
# S: Config ################################################

SrcFiles = filesWithExtension('./src', '.java')
JavacFlags = (
 # '-Xlint:unchecked' +
 ''
)

def TaskCompile():
  return {
    'name': 'compile',
    'deps': SrcFiles,
    'outs': ['./build'],

    'actions': [
      f'javac -d build {" ".join(SrcFiles)} {JavacFlags}',
    ],
  }

def TaskTest():
  return {
    'name': 'test',
    'deps': [TaskCompile],

    'capture': 1,
    'actions': [
      'java -cp build Test.RunTests',
    ],
  }

def TaskRun():
  return {
    'name': 'run',
    'deps': [TaskTest],
    'outs': ['./data/test.pkl.bz2'],

    'capture': 1,
    'actions': [
      rangesAction('test')
    ],
  }

def TaskFullExperiment():
  return {
    'name': 'full',
    'deps': [TaskCompile, TaskTest],
    'skipRun': True,

    'capture': 1,
    'actions': [
      rangesAction('case1'),
      rangesAction('case2'),
      rangesAction('small'),
      rangesAction('case3'),
      # copyPrevAction('small', 'medium'), rangesAction('medium'),
      # copyPrevAction('medium', 'large'), rangesAction('large'),
      # copyPrevAction('large', 'full'), rangesAction('full'),
    ],
  }

