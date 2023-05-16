UDOConfig = {
  'version': (1, 3, 0)
}

from pathlib import Path

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

SrcFiles = filesWithExtension('./src', '.java')

def TaskCompile():
  return {
    'name': 'compile',
    'deps': SrcFiles,
    'outs': ['./build'],

    'actions': [
      f'javac -d build {" ".join(SrcFiles)}',
    ],
  }

def TaskRun():
  return {
    'name': 'run',
    'deps': [TaskCompile],

    'capture': 1,
    'actions': [
      'java -cp build Main',
    ],
  }

