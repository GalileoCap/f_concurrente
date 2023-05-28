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
  if not force and os.path.isfile(fpath):
    return

  dfNoDup = df[[xaxis, yaxis, zaxis, color]].drop_duplicates() # TODO: Why this?
  if error is not None:
    dfNoDup = df[[xaxis, yaxis, error, zaxis, color]].drop_duplicates()
  fig = px.scatter(
    dfNoDup,
    x = xaxis,
    y = yaxis,
    animation_frame = zaxis,
    # animation_group = 'op',
    color = color,
    error_y = error,

    log_y = True,
    range_x = [dfNoDup[xaxis].min()-1, dfNoDup[xaxis].max()+1],
    range_y = [dfNoDup[yaxis].min(), dfNoDup[yaxis].max()],
  )

  fig.write_html(fpath)
