import sys
import utils
from utils import log

def logUsage():
  log('usage: convert_csv.py {INPUT_FILE} {OUTPUT_FILE} {MODE}\nWhere mode is either \'pkl2Csv\' or \'csv2Pkl\'', level = 'error')

if __name__ == '__main__':
  if len(sys.argv) < 4:
    logUsage()
    sys.exit(0)

  ipath, opath, mode = sys.argv[1:4]
  if mode.lower() == 'pkl2csv':
    utils.dfPkl2Csv(ipath, opath)
  elif mode.lower() == 'csv2pkl':
    utils.dfCsv2Pkl(ipath, opath)
  else:
    logUsage()
    sys.exit(1)
