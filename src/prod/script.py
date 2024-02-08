# luke hart @ colorado school of mines
# script template
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
import time

def func():
    load_dotenv()

    try:
        # TODO: implement script
        for i in range(100):
            time.sleep(0.2)
        return 0
    except Exception as e:
        print(f'Script failed: {e}')
        return 1
    
if __name__ == "__main__":
    func()