# luke hart @ colorado school of mines
# script template
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

def func():
    load_dotenv()
    logs = Path("../../logs")
    logs.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=logs / f"{datetime.now().isoformat().replace(':', '_')}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # TODO: implement script
        return 0
    except Exception as e:
        print(f'Script failed: {e}')
        return 1