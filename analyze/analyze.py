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
