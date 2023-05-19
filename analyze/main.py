import os
import json
import subprocess

if __name__ == '__main__':
  os.makedirs('../data', exist_ok = True)

  mode, logIn, logOut, newPost, nextPost, removePost, actions = 'monitor', 1, 1, 1, 1, 1, 5
  cmd = f'java -cp ../build ThreadPool {mode} {logIn} {logOut} {newPost} {nextPost} {removePost} {actions}'
  res = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE)
  res.check_returncode()

  data = dict()
  lines = res.stdout.decode('utf-8').split('\n')[:-1] # Last one is empty
  for out in (line.split(', ') for line in lines):
    mode = out[0]
    times = [int(t) for t in out[1:]]
    data[mode] = data.get(mode, []) + times

  fpath = f'{mode}_{logIn}_{logOut}_{newPost}_{nextPost}_{removePost}_{actions}.json'
  with open(os.path.join('../data', fpath), 'w') as fout:
    fout.write(json.dumps(data))

