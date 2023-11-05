import os
import sys

from main import main
from operators.OperatorConfig import OperatorConfig

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

if __name__ == '__main__':
    OperatorConfig()
    main()