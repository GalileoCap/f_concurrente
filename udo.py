# Default uDO file

UDOConfig = {
  'version': (1, 3, 0)
}

def TaskCompile():
  return {
    'name': 'compile',
    'deps': ['./src/main.java'],
    'outs': ['./build'],

    'actions': [
      'javac -d build src/main.java',
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

