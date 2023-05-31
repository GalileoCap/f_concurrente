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

def TaskPipenv():
  return {
    'name': 'pipenv',
    'deps': ['./analyze/Pipfile', './analyze/Pipfile.lock'],
    'outs': ['./analyze/.venv'],
    'clean': False,

    'actions': [
      'PIPENV_PIPFILE=./analyze/Pipfile pipenv install',
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
    'deps': [TaskTest, TaskPipenv],
    'outs': ['./data/test.pkl.bz2'],

    'capture': 1,
    'actions': [
      rangesAction('test')
    ],
  }

def TaskFullExperiment():
  cases = ['case1', 'case2', 'case3', 'small'] # , 'medium', 'large', 'full']
  return {
    'name': 'full',
    'deps': [TaskTest, TaskPipenv],
    'outs': [f'./data/{case}.pkl.bz2' for case in cases],
    'skipRun': True,
    'clean': False,

    'capture': 1,
    'actions': [rangesAction(case) for case in cases],
  }

def TaskEntrega():
  subdir = 'entrega'
  file = f'{subdir}_Cappella_Mansini.zip'

  return {
    'name': 'entrega',
    'outs': [file],
    'skipRun': True,

    'capture': 1,
    'actions': [
      f'mkdir -p {subdir}',
      f'cp -r ./README.md ./analyze ./consigna.pdf ./src ./udo.py informe.pdf ./data {subdir}',
      f'rm -r {subdir}/analyze/.venv',
      f'zip {file} {subdir} -r9',
      f'rm -r {subdir}',
    ],
  }
