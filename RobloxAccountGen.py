# Created by GiveUsername; aka nspe
# Todo: Captcha Solver
# Description:
     # // Can automatically create a number of unique roblox accounts. There are 7.992 × 10^11 unique names. Thats almost 8 Billion accounts.

import os
import sys
import time
from datetime import date
import threading
import string
import secrets
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import concurrent.futures

def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

Accounts = 1      # Accounts to create (Reccomened N/A | Depends on PC/Laptop Specs)
MaxWindows = 10   # Maximum Windows/Tabs (Reccomened 5-10)
ActualWindows = 0 # Maximum Actual Windows (Reccomened 0)

first_names_url = "https://raw.githubusercontent.com/GiveUsername/accgenner/main/first_names.txt"
last_names_url = "https://raw.githubusercontent.com/GiveUsername/accgenner/main/last_names.txt"
roblox_url = "https://www.roblox.com/"

status("Getting first names...")
session = requests.Session()
first_names_response = session.get(first_names_url)
status("Getting last names...")
last_names_response = session.get(last_names_url)

if first_names_response.status_code == 200 and last_names_response.status_code == 200:
    first_names = list(set(first_names_response.text.splitlines()))
    last_names = list(set(last_names_response.text.splitlines()))
else:
    status("Name loading failed. Re-Execute the script.")
    sys.exit()

files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts_{date.today()}.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin_{date.today()}.txt")

if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

def gen_password(length):
    status("Generating a password...")
    chars = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\\/¬|°_-[]*~+"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def gen_user(first_names, last_names):
    status("Generating a username...")
    first = secrets.choice(first_names)
    last = secrets.choice(last_names)
    full = f"{first}{last}_{secrets.choice([i for i in range(1, 999)]):03}"
    return full

def create_account(url, first_names, last_names):
    global ActualWindows
    try:
        status("Starting to create an account...")
        cookie_found = False
        username_found = False
        elapsed_time = 0

        status("Initializing webdriver...")
        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.minimize_window()
        driver.get(url)
        time.sleep(2)

        status("searching for items on the website")
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        status("Selecting day...")
        Selection = Select(day_dropdown)
        Selection.select_by_value(secrets.choice(days))
        time.sleep(0.3)

        status("Selecting month...")
        Selection = Select(month_dropdown)
        Selection.select_by_value(secrets.choice(months))
        time.sleep(0.3)

        status("Selecting year...")
        Selection = Select(year_dropdown)
        Selection.select_by_value(secrets.choice(years))
        time.sleep(0.3)

        while not username_found:
            status("Selecting username...")
            username = gen_user(first_names, last_names)
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            if username_error.text.strip() == "":
                username_found = True

        status("Selecting password...")
        password = gen_password(25)
        password_input.send_keys(password)
        time.sleep(0.3)

        status("Selecting gender...")
        gender = secrets.choice([1, 2])
        if gender == 1:
            male_button.click()
        else:
            female_button.click()
        time.sleep(0.5)

        status("Registering account...")
        register_button.click()
        time.sleep(3)

        try:
            driver.find_element("id", "GeneralErrorText")
            driver.quit()
            for i in range(360):
                status(f"Limit reached, waiting... {i+1}/{360}")
                time.sleep(1)
        except:
            pass

        while not cookie_found and elapsed_time < 180:
            status("Waiting for the cookie...")
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break
        if cookie_found:
            status("Printing Username...")
            result = [cookie.get('value'), username, password]
            save_account_info(result)
            save_altmanager_login(result)
            if result is not None:
                status("Successfully created!")
                time.sleep(3)
                ActualWindows -= 1
                status(f"Open Tabs: {ActualWindows}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                pass

    except:
        status(f"Open Tabs: {ActualWindows}")
        ActualWindows -= 1

def save_account_info(account_info):
    status("Saving account info...")
    with open(text_file, 'a') as file:
        file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")

def save_altmanager_login(account_info):
    with open(text_file2, 'a') as file:
        status("Saving account login (for alt manager)...")
        file.write(f"{account_info[1]},{account_info[2]}\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=MaxWindows) as executor:
    for _ in range(Accounts):
        executor.submit(create_account, roblox_url, first_names, last_names)
        time.sleep(1)
