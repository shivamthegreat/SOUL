from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from main import speak  # <-- Import speak instead of defining it
import time

def google_search(command):
    """
    Perform a Google search based on the command provided.
    """
    search_for = command.strip()
    if not search_for:
        print("No search query provided.")
        return

    speak("Okay sir!")
    speak(f"Searching for {search_for}")

    chrome_driver_path = 'D:/python/driver/chromedriver.exe'
    chrome_binary_path = 'C:\Users\KHUSHBOO\OneDrive\Desktop\elixir\driver\chromedriver.exe'

    service = Service(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.google.com')

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_for)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)

        title = driver.title
        speak(f"The page title is {title}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
