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
  cases = ['A', 'B', 'C', 'single', 'double', 'triple']

  return {
    'name': 'full',
    'deps': [TaskCompile, TaskTest],
    'outs': [f'./data/{case}.pkl.bz2' for case in cases] + [f'./out/{case}' for case in cases],
    'skipRun': True,
    'clean': False,

    'capture': 1,
    'actions': [rangesAction(case) for case in cases],
  }

