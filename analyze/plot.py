import plotly.express as px
import plotly.graph_objects as go
import time

import utils
from utils import log

def scatter(df, xaxis, yaxis, error, zaxis, color, fpath, *, layout = dict()):
  fig = px.scatter(
    df,
    x = xaxis,
    y = yaxis,
    animation_frame = zaxis,
    # animation_group = 'op',
    color = color,
    error_y = error,

    log_y = True,
    # range_x = [df[xaxis].min()-1, df[xaxis].max()+1],
    # range_y = [df[yaxis].min(), df[yaxis].max()],
  )

  fig.update_layout(**layout)

  if fpath[-4:] == 'html':
    fig.write_html(fpath)
  else:
    fig.write_image(fpath)
  return fig

def garbage():
  #NOTE: Fixes "Loading [MathJax]/extensions/MathMenu.js" showing in other pdf plots
  fig = go.Figure()
  fig.write_image(utils.imgPath('', 'garbage'))
  time.sleep(1)
