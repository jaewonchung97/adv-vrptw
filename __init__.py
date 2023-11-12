import os
import sys
import time

from main import main
from operators.OperatorConfig import OperatorConfig
from utils.load_dataset import load_dataset
from log.log_config import log

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    start = time.time()
    load_dataset()
    OperatorConfig()
    main()
    end = time.time()
    log.info(f"Origin Runtime: {end - start}")
