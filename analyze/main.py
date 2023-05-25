import sys

from cases import runAllCases
import utils
from utils import log

if __name__ == '__main__':
  if len(sys.argv) == 1:
    log(f'Please pass which ranges to use, one of: {list(utils.Ranges.keys())}', level = 'error')
    sys.exit(0)

  ranges = sys.argv[1]
  df = runAllCases(ranges, utils.Ranges[ranges])

  print(df.head(2), len(df), sep = '\n') # TODO: Analyze the data
