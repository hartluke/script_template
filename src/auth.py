from dotenv import load_dotenv
import requests
from getpass import getpass
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def csmsso_auth(driver):
    MINES_SSO_USERNAME = input("Enter your Mines SSO username: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    MINES_SSO_PASSWORD = getpass(prompt="Enter your Mines SSO password: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    # Write username and password to the .env file
    with open("../.env", 'a') as env:
        env.write(f"MINES_SSO_USERNAME='{MINES_SSO_USERNAME}'\n")
        env.write(f"MINES_SSO_PASSWORD='{MINES_SSO_PASSWORD}'\n")

    try:
        driver.get('https://my.mines.edu/')
        wait = WebDriverWait(driver, 20, poll_frequency=0.5)
        wait.until(EC.presence_of_element_located((By.ID, 'input28'))).send_keys(MINES_SSO_USERNAME)
        driver.find_element(by=By.CLASS_NAME, value="o-form-button-bar").click()

        wait.until(EC.presence_of_element_located((By.ID, 'input59'))).send_keys(MINES_SSO_PASSWORD)
        driver.find_element(by=By.CLASS_NAME, value='o-form-button-bar').click()

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'o-form-button-bar'))).click()

        # Pause and wait for user confirmation for MFA
        input("Please confirm Okta MFA on your phone, then press Enter to continue.")
      
        wait.until(EC.presence_of_element_located((By.ID, 'trust-browser-button'))).click()

        print(f'Successfully authenticated at {driver.current_url}')
        return 0
    except TimeoutException:
        print('Webdriver timed out during authentication')
        return 1
    except Exception as e:
        print(f'Failed to authenticate: {e}')
        return 1

def tdxapi_auth():
    load_dotenv()

    BEID = os.getenv('BEID')
    WEBSERVICEKEY = os.getenv('WEBSERVICEKEY')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    TOKEN = os.getenv('TOKEN')

    if not BEID or not WEBSERVICEKEY or not USERNAME or not PASSWORD or not TOKEN:
        BEID = input("Enter your Client ID: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        WEBSERVICEKEY = getpass(prompt="Enter your Client Secret: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        USERNAME = input("Enter your Username: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        PASSWORD = getpass(prompt="Enter your Password: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        TOKEN = getpass(prompt="Enter your Token: ")
        os.system('cls' if os.name == 'nt' else 'clear')

        # Write Client ID, Client Secret, Username, Password and Token to the .env file
        with open("../.env", 'a') as env:
            env.write(f"BEID='{BEID}'\n")
            env.write(f"WEBSERVICEKEY='{WEBSERVICEKEY}'\n")
            env.write(f"USERNAME='{USERNAME}'\n")
            env.write(f"PASSWORD='{PASSWORD}'\n")
            env.write(f"TOKEN='{TOKEN}'\n")

    # Basic API Authorization
    url = "https://helpcenter.mines.edu/SBTDWebApi/api/auth/login"
    data = {}
    headers = {
        'client_id': BEID,
        'client_secret': WEBSERVICEKEY,
        'username': USERNAME,
        'password': PASSWORD,
    }

    response = requests.request("POST", url, headers=headers, data=data)

    if response.status_code == 200:
        print('Successfully authenticated')
        return 0
    else:
        print(f'Failed to authenticate: {response.status_code}')
        return 1

if __name__ == "__main__":
    tdxapi_auth()