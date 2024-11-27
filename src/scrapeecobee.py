# scrapeecobee.py: script to log into the Ecobee website and scrape
# the thermostat names, setpoints, and current temperatures.
# The script will run indefinitely, printing the thermostat
# names, setpoints, and current temperatures periodically.
# This is to prove that our downstairs Lennox furnace is not working
# properly. 
#
# To install the required dependencies, run:
# pip3 install playwright
# playwright install
#
# Usage: python3 scrapeecobee.py
#
# Mark Riordan  2024-11-26

from playwright.sync_api import sync_playwright
import os
import sys
import time
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def add_to_line(line, text):
    if line:
        line += ','
    line += text
    return line

def scrape(page):
    # Select elements, each of which contains various info for one thermostat.
    elements = page.locator('div[data-qa-class="thermostat-tile"]')

    line = ''
    current_time = get_timestamp()
    line = add_to_line(line, current_time)
    #print(f'Current time: {current_time}')
    # Loop through the elements and print their text content
    for element in elements.all():
        name_element = element.locator('div[data-qa-class="interactive-tile_title"]').first
        thermostat_name = name_element.text_content()
        #print('thermostat name: ' + thermostat_name)
        line = add_to_line(line, thermostat_name)
        # Skip to the next div element
        next_div = name_element.locator('xpath=following-sibling::div').first
        
        # Find the next span element with data-qa-class="heat_setpoint" within the next div
        next_heat_setpoint = next_div.locator('span[data-qa-class="heat_setpoint"]').first
        setpoint = next_heat_setpoint.text_content()

        # Print the text content of the next heat setpoint element
        # print(f'  setpoint: {setpoint}')
        line = add_to_line(line, setpoint)

        temp_div = element.locator('div[data-qa-class="temperature"]').first
        temp_span = temp_div.locator('span').first
        temp = temp_span.text_content()
        # print(f'  current temperature: {temp}')
        line = add_to_line(line, temp)

    print(line)
    sys.stdout.flush()

def login(playwright):
    sys.stderr.write(f'{get_timestamp()} Logging in...\n')
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://auth.ecobee.com/u/login')

    # Fetch username and password from environment variables
    username = os.getenv('ECOBEE_USERNAME')
    password = os.getenv('ECOBEE_PASSWORD')
    if not username or not password:
        raise ValueError('Please set the ECOBEE_USERNAME and ECOBEE_PASSWORD environment variables')
    
    page.locator('#username').fill(username)
    page.locator('#password').fill(password)
    page.locator('[name="action"]').click()

    # Wait for navigation to complete
    page.wait_for_load_state('networkidle')
    return browser, page

def run_for_a_while(playwright):
    [browser,page] = login(playwright)
    for _ in range(40):
        scrape(page)
        time.sleep(30)
    sys.stderr.write(f'{get_timestamp()} Closing browser...\n')
    browser.close()

def run(playwright):
    while True:
        try:
            run_for_a_while(playwright)
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(30)

with sync_playwright() as playwright:
    run(playwright)
