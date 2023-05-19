import os

from cases import runAllCases
import utils
from utils import log

if __name__ == '__main__':
  os.makedirs('../data', exist_ok = True)
  
  ranges = utils.testRanges()
  # ranges = utils.smallRanges()
  # ranges = utils.mediumRanges()
  # ranges = utils.fullRanges()
  runAllCases(ranges)

  log('DONE', level = 'user')
