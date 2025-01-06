import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from controller.proxymesh import setup_driver_with_proxy,login_to_twitter
from controller.MongodbCrud import store_trends_in_db,generate_unique_id
import requests
import json

# Load environment variables
load_dotenv()

# Load credentials and MongoDB URI
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')


# Function to get the public IP address of the system
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json().get('ip')
        return ip
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        return None



def fetch_trending_topics(driver):
    driver.get('https://x.com/explore/tabs/trending')
    time.sleep(5)  # Allow time for the page to load

    try:
        print(f"Fetching Top Trends...")
        # Wait for elements with the unique identifier `data-testid="cellInnerDiv"`
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="cellInnerDiv"]'))
        )

        trends = []  # Store unique trend texts
        retries = 3  # Number of retries for scrolling

        for _ in range(retries):
            # Locate all trend items with `data-testid="cellInnerDiv"`
            trend_elements = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
    

            # Extract hashtags and post counts
            for trend in trend_elements:
                if(len(trends)>=5): return trends
                trend_text = trend.text.strip()

                # Simplified extraction of hashtags and post counts
                lines = trend_text.split('\n')
                print(lines[3])
                # for i, line in enumerate(lines):
                trends.append(lines[3])

            # Scroll to load more content
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)  # Allow time for new trends to load
            

     

        return trends

    except Exception as e:
        print(f"90 Error fetching trends: {e}")
        return []



# Create a function to run the script and show the results
def run_script_and_show_results(username,password):
    # Download the ChromeDriver
    # Setup driver with proxy
    driver, proxy_ip = setup_driver_with_proxy()


    try:
        # Login to Twitter
        login_to_twitter(driver,username,password)

        # Fetch trending topics
        trends = fetch_trending_topics(driver)

         # Get the public IP address of the system
        ip_address = get_public_ip()
        print('current ip',ip_address)

        # Store the trends in MongoDB
        store_trends_in_db(trends, ip_address)

        # Create the result structure for returning to Flask
        result = {
            'trends': trends,
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': ip_address,
            'record_json': {
                "unique_id": generate_unique_id(),
                "trend1": trends[0] if len(trends) > 0 else '',
                "trend2": trends[1] if len(trends) > 1 else '',
                "trend3": trends[2] if len(trends) > 2 else '',
                "trend4": trends[3] if len(trends) > 3 else '',
                "trend5": trends[4] if len(trends) > 4 else '',
            }
        }

        return result
    finally:
        driver.quit()  # Ensure the browser is closed after the script ends
