import os
import sys

from main import main
from operators.OperatorConfig import OperatorConfig
from utils.load_dataset import load_dataset

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    load_dataset()
    OperatorConfig()
    main()
