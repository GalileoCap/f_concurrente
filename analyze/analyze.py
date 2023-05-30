import os
import pandas as pd
import plotly.express as px
import itertools as itt

import utils
from utils import log, OUTDIR

def analyze(df, name):
  cols = ['mode', 'actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads']
  df = df.groupby(cols).mean().reset_index()
  print(df.head())

  df['totalThreads'] = df['logIn_threads'] + df['logOut_threads'] + df['apiRequest_threads']
  df['totalActions'] = df['actions'] * df['totalThreads']

  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(
      df,
      f'{op}_threads', f'{op}_meanTime', None, 'totalThreads', 'mode',
      utils.htmlPath(name, f'{op}_op')
    )
    foo(
      df,
      f'{op}_threads', 'totalTime', None, 'totalThreads', 'mode', 
      utils.htmlPath(name, f'{op}_total')
    )

    foo(
      df,
      'totalThreads', f'{op}_meanTime', None, 'actions', 'mode',
      utils.htmlPath(name, f'{op}_actions')
    )
    foo(
      df,
      'totalThreads', f'{op}_meanTime', None, 'totalActions', 'mode',
      utils.htmlPath(name, f'{op}_totalActions')
    )

  foo(
    df,
    'totalThreads', 'totalTime', None, 'actions', 'mode',
    utils.htmlPath(name, 'total_actions')
  )
  foo(
    df,
    'totalThreads', 'totalTime', None, 'totalActions', 'mode',
    utils.htmlPath(name, 'total_totalActions')
  )

  data = []
  for current in ['logIn', 'logOut', 'apiRequest']:
    threadsCol = f'{current}_threads'
    for totalThreads in range(df['totalThreads'].min(), df['totalThreads'].max()+1):
      for currentThreads in range(df[threadsCol].min(), df[threadsCol].max()+1): # NOTE: Assumes all types have the same range
        _df = df[
          (df['totalThreads'] == totalThreads) &
          (df[threadsCol] == currentThreads)
        ]
        if len(_df) > 0:
          stats = _df[['logIn_meanTime', 'logOut_meanTime', 'apiRequest_meanTime', 'totalTime']].agg(['mean', 'std'])
          _data = {'op': current, 'totalThreads': totalThreads, 'opThreads': currentThreads}
          for idx, row in stats.iterrows():
            for col, value in row.items():
              _data[f'{col}_{idx}'] = value
          data.append(_data)

  df = pd.DataFrame(data)

  df['opThreads%'] = df['opThreads'] / df['totalThreads'] * 100

  bar(df, 'opThreads', 'totalTime_mean', None, None, 'op', utils.htmlPath(name, 'opsTimes'))
  bar(df, 'opThreads%', 'totalTime_mean', None, None, 'op', utils.htmlPath(name, 'opsTimes%'))
  # foo(df, 'opThreads', 'totalTime_mean', None, 'totalThreads', 'op', utils.htmlPath(name, 'opsTimes')) # TODO: opTime

  uglyPlots(df, name)

def uglyPlots(df, name):
  xaxis = ['actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads', 'totalThreads', 'totalActions']
  yaxis = ['logIn_medianTime', 'logIn_meanTime', 'logIn_stdTime', 'logOut_medianTime', 'logOut_meanTime', 'logOut_stdTime', 'apiRequest_medianTime', 'apiRequest_meanTime', 'apiRequest_stdTime', 'totalTime']
  zaxis = xaxis
  color = ['mode']

  log('Ugly plots:', len(xaxis) * len(yaxis) * len(zaxis) * len(color), level = 'debug')
  for c1, c2, c3, c4 in itt.product(xaxis, yaxis, zaxis, color):
    fpath = utils.htmlPath(f'{name}_ugly', f'{c1}__{c2}__{c3}__{c4}')
    try: foo(df, c1, c2, None, c3, c4, fpath)
    except: pass

def foo(df, xaxis, yaxis, error, zaxis, color, fpath, force = False):
  dfNoDup = df[[xaxis, yaxis, zaxis, color]].drop_duplicates() # TODO: Why this?
  if error is not None:
    dfNoDup = df[[xaxis, yaxis, error, zaxis, color]].drop_duplicates()
  return bar(dfNoDup, xaxis, yaxis, error, zaxis, color, fpath, force = force)

def bar(df, xaxis, yaxis, error, zaxis, color, fpath, force = False):
  if not force and os.path.isfile(fpath):
    return

  fig = px.scatter(
    df,
    x = xaxis,
    y = yaxis,
    animation_frame = zaxis,
    # animation_group = 'op',
    color = color,
    error_y = error,

    log_y = True,
    range_x = [df[xaxis].min()-1, df[xaxis].max()+1],
    range_y = [df[yaxis].min(), df[yaxis].max()],
  )

  fig.write_html(fpath)

