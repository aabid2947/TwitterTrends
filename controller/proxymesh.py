from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv()

def create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
            }}
        }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy_username}",
                password: "{proxy_password}"
            }}
        }};
    }}
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {{urls: ["<all_urls>"]}},
                ['blocking']
    );
    """

    # with open("controller/manifest.json", "w") as f:
    #     f.write(manifest_json)

    # with open("controller/background.js", "w") as f:
    #     f.write(background_js)

def setup_driver_with_proxy():
    try:
        PROXY_HOST = os.getenv('PROXYMESH_HOST')
        PROXY_PORT = os.getenv('PROXYMESH_PORT')
        PROXY_USERNAME = os.getenv('PROXYMESH_USERNAME')
        PROXY_PASSWORD = os.getenv('PROXYMESH_PASSWORD')



        create_proxy_extension(PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD)

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--load-extension=.')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        proxy_ip = f"{PROXY_HOST}:{PROXY_PORT}"
        return driver, proxy_ip


    except Exception as e:
        print(f"Driver setup error: {str(e)}")
        return None

def login_to_twitter(driver,username,password):
    try:
        print("Starting Twitter login process...")
        driver.get('https://twitter.com/i/flow/login')
        wait = WebDriverWait(driver, 20)

        # Step 1: Enter username
        print("Entering username...")
        username_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_field.send_keys(username)
        next_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[text()='Next']")))
        next_button.click()
        time.sleep(2)

        # Step 2: Enter password
        print("Entering password...")
        password_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[type="password"]')))
        password_field.send_keys(password)
        login_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[text()='Log in']")))
        login_button.click()

        # Step 3: Verify login
        print("Verifying login...")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="primaryColumn"]')))
        print("Login successful!")
        return True

    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

def test_proxy_connection():
    driver = setup_driver_with_proxy()
    if driver:
        try:
            if login_to_twitter(driver):
                print("Testing proxy connection...")
                driver.get('https://api.ipify.org?format=json')
                
                wait = WebDriverWait(driver, 15)
                body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
                
                print(f"Current IP: {body.text}")
                time.sleep(2)
                
        except Exception as e:
            print(f"Connection error: {str(e)}")
        
        finally:
            driver.quit()
    else:
        print("Failed to initialize driver")


  