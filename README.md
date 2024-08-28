# MittArv_Assignment

# Selenium Form Automation Script

## Description

This script automates filling out and submitting a registration form on the Mitt Arv website using Selenium. It peSeleniumhe following actions:
1. Opens the specified registration URL.
2. Waits for the registration form to load.
3. Fill out the form fields for Name, Email, and Phone Number.
4. Click the "Get OTP" button to complete the registration process.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python**: The script is written in Python. Could you make sure python 3. x is installed on your system? You can download Python from [pythPython](https://www.python.org/downloads/).

2. **Selenium**: The Selenium library for Python is required using pip:

   ```bash
   pip install selenium

3. **Seleniumhrome**: Ensure that your system has installed Google Chrome. The version of ChromeDriver should match your Chrome browser version.

## Running the Script
**Clone or Download the Script**: Save the provided Python script to a file, for example, automate_form.py.

**Open Terminal or Command Prompt**: Navigate to the directory where the script is located.

**Run the Script**: Execute the script with the required command-line arguments for name, email, and phone. For example:

bash
python automate_form.py --name " Name " --email "example@gmail.com" --phone "123456789"
Could you replace the values with your actual details?

**Platform Compatibility**
The script is designed to run on any platform where Python, Selenium, and ChromeDriver are supported, including:

**Windows**

**Notes**
**Headless Mode**: If you want to run the browser in headless mode (without opening a visible browser window), uncomment the line chrome_options.add_argument("--headless") in the script.

**Pop-Up Handling**: The script assumes that any pop-up present can be closed. If the pop-up is different or additional handling is needed, you should adjust the script accordingly.

**Logging**: The script uses Python's logging Python'so output information about its progress. Could you check the terminal or command prompt for these log messages?

**Here, otp_fetch.py and test.py files are extra files to fetch the OTP from the mail and update it in the registration form to create the registration form successfully.
If you have any issues or need additional modifications, refer to the Selenium documentation or consult Python's official doPython'sion.
