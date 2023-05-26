import os
import pandas as pd

import utils
from utils import log, OUTDIR

def analyze(df, name):
  # print(df.describe(), df.columns, sep = '\n')

  df['totalThreads'] = df['logIn_threads'] + df['logOut_threads'] + df['apiRequest_threads']

  data = []
  for totalThreads in range(df['totalThreads'].min(), df['totalThreads'].max()+1):
    for currentThreads in range(df['logIn_threads'].min(), df['logIn_threads'].max()+1): # NOTE: Assumes all types have the same range
      for current in ['logIn_threads', 'logOut_threads', 'apiRequest_threads']:
        _df = df[
          (df['totalThreads'] == totalThreads) &
          (df[current] == currentThreads)
          # (df[current] == currentThreads) &
          # (df['logOut_threads'] == df['apiRequest_threads'])
        ]
        if len(_df) > 0:
          stats = _df[['logIn_meanTime', 'logOut_meanTime', 'apiRequest_meanTime', 'totalTime']].agg(['mean', 'std'])
          _data = {'op': current, 'totalThreads': totalThreads, 'opThreads': currentThreads}
          for idx, row in stats.iterrows():
            for col, value in row.items():
              _data[f'{col}_{idx}'] = value
          data.append(_data)

  df = pd.DataFrame(data)
  print(df.describe(), sep = '\n')
