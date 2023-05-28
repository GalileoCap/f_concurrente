import os
import pandas as pd
import plotly.express as px

import utils
from utils import log, OUTDIR

def analyze(df, name):
  cols = ['mode', 'actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads']
  df = df.groupby(cols).mean().reset_index()
  print(df.head())

  df['totalThreads'] = df['logIn_threads'] + df['logOut_threads'] + df['apiRequest_threads']

  for op in ['logIn', 'logOut', 'apiRequest']:
    xaxis, zaxis, color = f'{op}_threads', 'totalThreads', 'mode'
    fpath = os.path.join(OUTDIR, f'{op}.html')
    foo(df, xaxis, f'{op}_meanTime', zaxis, color, fpath)
    # foo(df, xaxis, 'totalTime', zaxis, color, fpath)

def foo(df, xaxis, yaxis, zaxis, color, fpath):
  dfNoDup = df[[xaxis, yaxis, zaxis, color]].drop_duplicates() # TODO: Why this?
  fig = px.scatter(
    dfNoDup,
    x = xaxis,
    y = yaxis,
    animation_frame = zaxis,
    # animation_group = 'op',
    color = color,

    log_y = True,
    range_x = [dfNoDup[xaxis].min()-1, dfNoDup[xaxis].max()+1],
    range_y = [dfNoDup[yaxis].min(), dfNoDup[yaxis].max()],
  )

  os.makedirs(OUTDIR, exist_ok = True)
  fig.write_html(fpath)

if False:
  # print(df.describe(), df.columns, sep = '\n')

  data = []
  for totalThreads in range(df['totalThreads'].min(), df['totalThreads'].max()+1):
    for currentThreads in range(df['logIn_threads'].min(), df['logIn_threads'].max()+1): # NOTE: Assumes all types have the same range
      for current in ['logIn_threads', 'logOut_threads', 'apiRequest_threads']:
        _df = df[
          (df['totalThreads'] == totalThreads) &
          (df[current] == currentThreads)
        ]
        if len(_df) > 0:
          stats = _df[['logIn_meanTime', 'logOut_meanTime', 'apiRequest_meanTime', 'totalTime']].agg(['mean', 'std'])
          _data = {'op': current, 'totalThreads': totalThreads, 'opThreads': currentThreads}
          for idx, row in stats.iterrows():
            for col, value in row.items():
              _data[f'{col}_{idx}'] = value
          data.append(_data)

  df = pd.DataFrame(data)
  print(df.describe())
  fig = px.scatter(
    df,
    x = 'opThreads',
    y = 'totalTime_mean',
    animation_frame = 'totalThreads',
    # animation_group = 'op',
    color = 'op',

    log_y = True,
    range_x = [df['opThreads'].min()-1, df['opThreads'].max()+1],
    range_y = [df['totalTime_mean'].min(), df['totalTime_mean'].max()],
  )

  os.makedirs(OUTDIR, exist_ok = True)
  fpath = os.path.join(OUTDIR, 'anim.html')
  fig.write_html(fpath)
