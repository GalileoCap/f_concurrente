import os
import sys
import pandas as pd
import itertools as itt

import plot
import utils
from utils import log

def analyze(df, name):
  cols = ['mode', 'actions', 'logIn_threads', 'logOut_threads', 'apiRequest_threads']
  df = df.groupby(cols).mean().reset_index()

  df['totalThreads'] = df['logIn_threads'] + df['logOut_threads'] + df['apiRequest_threads']
  df['totalActions'] = df['actions'] * df['totalThreads']

  specificPlots(df, name)
  genericPlots(df, name)
  opTimePlots(df, name)
  # uglyPlots(df, name)

def specificPlots(df, name):
  plot.garbage() #NOTE: Fixes "Loading [MathJax]/extensions/MathMenu.js" showing in other pdf plots

  fbase = f'{name}_specific'
  if name == 'small':
    smallPlots(df, fbase)
  elif name == 'case1':
    case1Plots(df, fbase)
  elif name == 'case2':
    case2Plots(df, fbase)
  elif name == 'case3':
    case3Plots(df, fbase)

def smallPlots(df, fbase):
  _df = df.copy()

  # df = _df[(_df['actions'] == 10) & (5 <= _df['totalThreads']) & (_df['totalThreads'] < 30)].copy()
  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(df, 'totalThreads', f'{op}_meanTime', None, None, 'mode', utils.imgPath(fbase, f'{op}_meanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = 'Threads totales',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    )) # TODO: Fpath

  foo(df, 'totalThreads', 'totalTime', None, None, 'mode', utils.imgPath(fbase, 'total'), layout = dict(
    # title = 'Tiempo promedio para ejecutar todas las acciones',
    xaxis_title = 'Threads totales',
    yaxis_title = 'Tiempo total promedio (ns)',
    legend_title = 'Modo de sincronización',
  )) # TODO: Fpath

  # df = _df[(_df['actions'] == 10) & (5 <= _df['totalThreads']) & (_df['totalThreads'] < 30)]
  for op in ['logIn', 'logOut', 'apiRequest']:
    df[f'{op}_threads%'] = df[f'{op}_threads'] / df['totalThreads'] * 100
    df[f'{op}_threads%'] = df[f'{op}_threads%'].round()
    foo(df, f'{op}_threads%', 'totalTime', False, None, 'mode', utils.imgPath(fbase, f'{op}pct_totalTime'), layout = dict( # TODO: Error = False or None?
      # title = 'Tiempo promedio para ejecutar todas las acciones',
      xaxis_title = f'Porcentaje de threads ejecutando {op}',
      yaxis_title = 'Tiempo total promedio (ns)',
      legend_title = 'Modo de sincronización',
    )) # TODO: Fpath

def case1Plots(df, fbase):
  _df = df.copy()

  # df = _df[(_df['actions'] == 10) & (5 <= _df['totalThreads']) & (_df['totalThreads'] < 30)].copy()
  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(df, f'{op}_threads', f'{op}_meanTime', False, None, 'mode', utils.imgPath(fbase, f'{op}Threads_meanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = f'Porcentaje de threads ejecutando {op}',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    ))
    foo(df, f'{op}_threads', 'totalTime', False, None, 'mode', utils.imgPath(fbase, f'{op}Threads_totalTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = f'Porcentaje de threads ejecutando {op}',
      yaxis_title = f'Tiempo promedio total (ns)',
      legend_title = 'Modo de sincronización',
    ))
    foo(df, 'actions', f'{op}_meanTime', None, None, 'mode', utils.imgPath(fbase, f'actions_{op}_meanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = 'Acciones por thread',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    )) # TODO: Fpath
    foo(df, 'totalActions', f'{op}_meanTime', None, None, 'mode', utils.imgPath(fbase, f'totalActions_{op}_meanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = 'Acciones totales',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    )) # TODO: Fpath

  foo(df, 'actions', 'totalTime', None, None, 'mode', utils.imgPath(fbase, 'actions_total'), layout = dict(
    # title = 'Tiempo promedio para ejecutar todas las acciones',
    xaxis_title = 'Acciones por thread',
    yaxis_title = 'Tiempo total promedio (ns)',
    legend_title = 'Modo de sincronización',
  )) # TODO: Fpath
  foo(df, 'totalActions', 'totalTime', None, None, 'mode', utils.imgPath(fbase, 'totalActions_total'), layout = dict(
    # title = 'Tiempo promedio para ejecutar todas las acciones',
    xaxis_title = 'Acciones totales',
    yaxis_title = 'Tiempo total promedio (ns)',
    legend_title = 'Modo de sincronización',
  )) # TODO: Fpath

def case2Plots(df, fbase):
  _df = df.copy()

  df = _df[(_df['actions'] == 100)]
  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(df, 'totalThreads', f'{op}_meanTime', None, None, 'mode', utils.imgPath(fbase, f'totalThreads_{op}MeanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = f'Cantidad total de threads',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    ))

  foo(df, 'totalThreads', 'totalTime', None, None, 'mode', utils.imgPath(fbase, f'totalThreads_totalTime'), layout = dict(
    # title = 'Tiempo promedio para ejecutar una acción',
    xaxis_title = f'Cantidad total de threads',
    yaxis_title = f'Tiempo promedio en total (ns)',
    legend_title = 'Modo de sincronización',
  ))

def case3Plots(df, fbase):
  _df = df.copy()

  for op in ['logIn', 'logOut', 'apiRequest']:
    foo(df, 'totalThreads', f'{op}_meanTime', False, None, 'mode', utils.imgPath(fbase, f'totalThreads_{op}MeanTime'), layout = dict(
      # title = 'Tiempo promedio para ejecutar una acción',
      xaxis_title = f'Cantidad de threads en total',
      yaxis_title = f'Tiempo promedio por {op} (ns)',
      legend_title = 'Modo de sincronización',
    ))

  foo(df, 'totalThreads', 'totalTime', False, None, 'mode', utils.imgPath(fbase, f'totalThreads_totalTime'), layout = dict(
    # title = 'Tiempo promedio para ejecutar una acción',
    xaxis_title = f'Cantidad de threads en total',
    yaxis_title = f'Tiempo promedio en total (ns)',
    legend_title = 'Modo de sincronización',
  ))

def genericPlots(df, name):
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

def opTimePlots(df, name):
  data = []
  for mode, current, totalThreads in itt.product(df['mode'].unique(), ['logIn', 'logOut', 'apiRequest'], range(df['totalThreads'].min(), df['totalThreads'].max()+1)):
    threadsCol = f'{current}_threads'
    for currentThreads in range(df[threadsCol].min(), df[threadsCol].max()+1):
      _df = df[
        (df['mode'] == mode) &
        (df['totalThreads'] == totalThreads) &
        (df[threadsCol] == currentThreads)
      ]
      if len(_df) > 0:
        stats = _df[['logIn_meanTime', 'logOut_meanTime', 'apiRequest_meanTime', 'totalTime']].agg(['mean', 'std'])
        _data = {'mode': mode, 'op': current, 'totalThreads': totalThreads, 'opThreads': currentThreads}
        for idx, row in stats.iterrows():
          for col, value in row.items():
            _data[f'{col}_{idx}'] = value
        data.append(_data)

  df = pd.DataFrame(data)

  df['opThreads%'] = df['opThreads'] / df['totalThreads'] * 100

  foo(df, 'opThreads', 'totalTime_mean', None, 'mode', 'op', utils.htmlPath(name, 'opsTimes'))
  foo(df, 'opThreads%', 'totalTime_mean', None, 'mode', 'op', utils.htmlPath(name, 'opsTimes%'))
  foo(df, 'opThreads', 'totalTime_mean', None, 'op', 'mode', utils.htmlPath(name, 'opsTimes_alt'))
  foo(df, 'opThreads%', 'totalTime_mean', None, 'op', 'mode', utils.htmlPath(name, 'opsTimes%_alt'))
  # foo(df, 'opThreads', 'totalTime_mean', None, 'totalThreads', 'op', utils.htmlPath(name, 'opsTimes')) # TODO: opTime

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

def foo(df, xaxis, yaxis, error, zaxis, color, fpath, *, force = False, layout = dict()):
  if not force and os.path.isfile(fpath):
    return

  cols = [col for col in [xaxis, yaxis, error, zaxis, color] if col not in [None, False]]
  _df = df[cols].drop_duplicates()

  mean_cols = [col for col in [xaxis, zaxis, color] if col not in [None, False]]
  df = _df.groupby(mean_cols).mean().reset_index()
  if error is False:
    error = None
  elif error is None:
    error = 'yaxis_std'
    df[error] = _df.groupby(mean_cols).std().reset_index()[yaxis]

  return plot.scatter(df, xaxis, yaxis, error, zaxis, color, fpath, layout = layout)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    log(f'Please pass which ranges to use, one of: {list(utils.Ranges.keys())}', level = 'error')
    sys.exit(0)

  ranges = sys.argv[1]
  df = utils.readDf(utils.dfPath(ranges))
  analyze(df, ranges)
