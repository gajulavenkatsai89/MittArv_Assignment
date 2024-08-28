from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import argparse

# Set up logging to show information messages
logging.basicConfig(level=logging.INFO)

# Set up Chrome options for the Selenium WebDriver
chrome_options = Options()
# Uncomment the line below if you want to run the browser in headless mode (without GUI)
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ssl-protocol=any')
chrome_options.add_argument('--disable-extensions')

# Path to the ChromeDriver executable
chromedriver_path = 'chromedriver'

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

def main(name, email, phone_number):
    """
    Automates the process of filling out and submitting a registration form on the Mitt Arv website.
    
    Args:
    - name (str): The name to be entered in the registration form.
    - email (str): The email address to be entered in the registration form.
    - phone_number (str): The phone number to be entered in the registration form.
    """
    try:
        # Open the Mitt Arv registration page
        driver.get("https://www.mittarv.com/register/referralcode/WEBSITE")
        
        # Wait for the registration form to load on the page
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "details_form"))
        )

        # Find the registration form element on the page
        form = driver.find_element(By.CLASS_NAME, "details_form")
        logging.info("Found the details form")
        
        # Locate the Name field within the form and input the provided name
        name_field = form.find_element(By.CLASS_NAME, "name_field").find_element(By.TAG_NAME, "input")
        name_field.send_keys(name)
        logging.info("Found Name field and sent the input")

        # Locate the Email field within the form and input the provided email
        email_field = form.find_element(By.CLASS_NAME, "email_field").find_element(By.TAG_NAME, "input")
        email_field.send_keys(email)
        logging.info("Found Email field and sent the input")

        # Locate the Phone Number field within the form and input the provided phone number
        phone_field = form.find_element(By.CLASS_NAME, "phone_number_field").find_element(By.TAG_NAME, "input")
        phone_field.send_keys(phone_number)
        logging.info("Found Phone Number field and sent the input")

        # Locate and click the "Get OTP" button to complete the registration process
        otp_button = form.find_element(By.ID, "t2")
        otp_button.click()
        logging.info("Clicked the 'Get OTP' button")

    finally:
        # Wait for a few seconds to ensure any post-submission processes are completed
        time.sleep(5)
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Set up argument parsing to allow command-line arguments for the script
    parser = argparse.ArgumentParser(description="Automate form filling on the Mitt Arv website")
    parser.add_argument('--name', required=True, help="Your name")
    parser.add_argument('--email', required=True, help="Your email address")
    parser.add_argument('--phone', required=True, help="Your phone number")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the parsed command-line arguments
    main(args.name, args.email, args.phone)
