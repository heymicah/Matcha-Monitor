from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import requests
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# ENV Variables
DRIVER_PATH = os.getenv("DRIVER")
WEBHOOK = os.getenv("WEBHOOK_URL")

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=chrome_options)

# Discord Integration
webhook = WEBHOOK

# URL to monitor
url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1/"

def main():
    try:
        while(True):
            driver.get(url)
            timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            try:
                wait = WebDriverWait(driver, 5)
                p_element = driver.find_element(By.CSS_SELECTOR, "p.stock.out-of-stock")
                stock_status = p_element.text
            except:
                try:
                    button_element = driver.find_element(By.CSS_SELECTOR, "button.single_add_to_cart_button")
                    if button_element.text == "Add To Cart":
                        stock_status = "In Stock"
                        instock_notification(webhook, url)
                    else:
                        stock_status = "Unknown"
                except:
                    stock_status = "Unknown"

            print(f"[{timestamp}] Stock Status: {stock_status}")
            if stock_status == "In Stock":
                break
            time.sleep(600)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

def instock_notification(webhook, url):
    message = {
    'content': f'''IN STOCK GO GO GO
    Link: {url}
                '''
    }
    # Send the POST request to the webhook URL
    response = requests.post(webhook, json=message)

    # Check the response status
    if response.status_code == 204:
        print('Webhook Sent')
    else:
        print(f'Failed to send message. Status code: {response.status_code}')
        print('Response:', response.text)

if __name__ == '__main__':
    main()
