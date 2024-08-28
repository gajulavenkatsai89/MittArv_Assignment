import os.path
import re
import time
import logging
import base64
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set Chrome options
chrome_options = Options()
# Uncomment the line below if you want to run in headless mode
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ssl-protocol=any')
chrome_options.add_argument('--disable-extensions')

# Path to the chromedriver executable
chromedriver_path = 'chromedriver'

# Initialize the webdriver
driver = webdriver.Chrome(options=chrome_options)


def main(name, email_user, email_pass, phone_number):
    try:
        # Open the website
        driver.get("https://www.mittarv.com/register/referralcode/WEBSITE")
        
        # Wait for the registration page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "details_form"))
        )

        # Find the form
        form = driver.find_element(By.CLASS_NAME, "details_form")
        logging.info("Found the details form")
        
        # Fill out the registration form
        name_field = form.find_element(By.CLASS_NAME, "name_field").find_element(By.TAG_NAME, "input")
        name_field.send_keys(name)
        logging.info("Found Name field and sent the input")

        email_field = form.find_element(By.CLASS_NAME, "email_field").find_element(By.TAG_NAME, "input")
        email_field.send_keys(email_user)
        logging.info("Found Email field and sent the input")

        phone_field = form.find_element(By.CLASS_NAME, "phone_number_field").find_element(By.TAG_NAME, "input")
        phone_field.send_keys(phone_number)
        logging.info("Found Phone Number field and sent the input")

        # Click the "Get OTP" button
        otp_button = form.find_element(By.ID, "t2")
        otp_button.click()
        logging.info("Clicked the 'Get OTP' button")

        # Wait for OTP email and retrieve it with retries
        max_retries = 5
        for attempt in range(max_retries):
            try:
                otp = get_otp_from_email()
                if otp:
                    logging.info(f"Retrieved OTP: {otp}")
                    break
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(30)  # Wait before retrying
        else:
            logging.error("Failed to retrieve OTP after several attempts")
            return

        # Enter the OTP into the OTP fields
        otp_fields = driver.find_elements(By.CSS_SELECTOR, ".otp_field input")
        for i, digit in enumerate(otp):
            otp_fields[i].send_keys(digit)
        logging.info("Entered the OTP into the OTP fields")

        # Click the "Sign In" button
        sign_in_button = driver.find_element(By.ID, "t2")
        sign_in_button.click()
        logging.info("Clicked the 'Sign In' button")

    finally:
        # Close the browser
        time.sleep(5)  # Wait for any post-submission processes
        driver.quit()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Automate form filling and OTP entry on the Mitt Arv website")
    parser.add_argument('--name', required=True, help="Your name")
    parser.add_argument('--email', required=True, help="Your email address")
    parser.add_argument('--password', required=True, help="Your email password or app-specific password")
    parser.add_argument('--phone', required=True, help="Your phone number")

    args = parser.parse_args()

    # Call the main function with command-line arguments
    main(args.name, args.email, args.password, args.phone)
