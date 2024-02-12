# luke hart @ colorado school of mines
# script template
from dotenv import load_dotenv

def func():
    load_dotenv()

    try:
        # TODO: implement script
        return 0
    except Exception as e:
        print(f'Script failed: {e}')
        return 1
    
if __name__ == "__main__":
    func()