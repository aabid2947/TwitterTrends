import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from proxymesh import setup_driver_with_proxy,login_to_twitter


# Load environment variables
load_dotenv()

# Load credentials and MongoDB URI
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')



# Create a function to generate a unique ID for each run
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))




def fetch_trending_topics(driver):
    driver.get('https://x.com/explore/tabs/trending')
    time.sleep(5)  # Allow time for the page to load

    try:
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
                trend_text = trend.text.strip()

                # Simplified extraction of hashtags and post counts
                lines = trend_text.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('#') :
                        trends.append(line)

            # Scroll to load more content
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)  # Allow time for new trends to load

     

        print("Output saved to 'trending_topics.json'")
        return trends

    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []


# Create a function to store the trends in MongoDB
def store_trends_in_db(trends, ip_address):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['trending_topics']
    
    # Fill missing trends with placeholders if fewer than 5 are found
    while len(trends) < 5:
        trends.append('No data available')

    unique_id = generate_unique_id()
    
    record = {
        'unique_id': unique_id,
        'trend': trends,
        'date_time': datetime.now(),
        'ip_address': ip_address
    }
    print(record)

    collection.insert_one(record)
    client.close()

# Create a function to run the script and show the results
def run_script_and_show_results():
    # Download the ChromeDriver
    driver = setup_driver_with_proxy()


    try:
        # Login to Twitter
        login_to_twitter(driver)

        # Fetch trending topics
        trends = fetch_trending_topics(driver)

        # Example IP address (we will use a placeholder here)
        ip_address = "192.168.1.1"

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

        print(f"Result to return: {result}")

        return result
    finally:
        driver.quit()  # Ensure the browser is closed after the script ends
