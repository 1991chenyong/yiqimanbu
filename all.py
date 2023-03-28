import pytest
import os
import time
from common.send_email import send_email


if __name__ == '__main__':
    pytest.main()
    time.sleep(1)
    os.system("allure generate ./temps -o ./reports --clean")
    # send_email('./reports/index.html')