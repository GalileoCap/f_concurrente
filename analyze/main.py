import os

from cases import runAllCases
import utils
from utils import log

if __name__ == '__main__':
  ranges = utils.testRanges()
  # ranges = utils.smallRanges()
  # ranges = utils.mediumRanges()
  # ranges = utils.fullRanges()

  data = runAllCases(ranges)

  print(list(data.items())[0]) # TODO: Analyze the data
