import sys

from cases import runAllCases
import utils
from utils import log

if __name__ == '__main__':
  if len(sys.argv) == 1:
    log(f'Please pass which ranges to use, one of: {list(utils.Ranges.keys())}', level = 'error')
    sys.exit(0)

  ranges = sys.argv[1]
  log('Running:', ranges, level = 'user')

  data = runAllCases(utils.Ranges[ranges])

  print(list(data.items())[0]) # TODO: Analyze the data
