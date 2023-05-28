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
  df['totalActions'] = df['actions'] * df['totalThreads']

  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(df, f'{op}_threads', f'{op}_meanTime', 'totalThreads', 'mode', utils.htmlPath(f'{op}_op'))
    foo(df, f'{op}_threads', 'totalTime', 'totalThreads', 'mode', utils.htmlPath(f'{op}_total'))

    foo(df, 'totalThreads', f'{op}_meanTime', 'actions', 'mode', utils.htmlPath(f'{op}_actions'))
    foo(df, 'totalThreads', f'{op}_meanTime', 'totalActions', 'mode', utils.htmlPath(f'{op}_totalActions'))

  foo(df, 'totalThreads', 'totalTime', 'actions', 'mode', utils.htmlPath('total_actions'))
  foo(df, 'totalThreads', 'totalTime', 'totalActions', 'mode', utils.htmlPath('total_totalActions'))

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
