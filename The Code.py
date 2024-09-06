#Made By Mesbah (Lamp)

import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import requests

# Specify the path to your WebDriver
driver_path = 'D:/Games New/chromedriver-win64/chromedriver.exe'
download_folder = 'C:/Users/Dell/Downloads/Arduino_Files'

# Create the download folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Set Chrome options to define the download folder
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

service = Service(executable_path=driver_path)

# Open the Arduino Libraries website
website_url = 'https://www.arduinolibraries.info/libraries'

def wait_for_download(download_folder, timeout=20):
    """Wait for a file to be downloaded to the specified folder and log details."""
    end_time = time.time() + timeout
    files_before = set(os.listdir(download_folder))
    while time.time() < end_time:
        files_after = set(os.listdir(download_folder))
        new_files = files_after - files_before
        if new_files:  # If there are new files
            new_file = list(new_files)[0]
            new_file_path = os.path.join(download_folder, new_file)
            while True:
                if os.path.exists(new_file_path):
                    if os.path.getsize(new_file_path) > 0:  # Check if file is non-empty
                        print(f"File downloaded: {new_file} (Size: {os.path.getsize(new_file_path)} bytes)")
                        return True
                time.sleep(3)  # Check every few seconds
        time.sleep(6)  # Check again in 6 seconds
    print("Download timed out.")
    return False

def download_file(download_link):
    try:
        response = requests.get(download_link, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        file_name = download_link.split("/")[-1]
        file_path = os.path.join(download_folder, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully: {file_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")
        return False

def initialize_driver():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website_url)
    return driver

def process_library_links(start_index=0, reset_every=100):
    driver = initialize_driver()
    try:
        processed_count = 0
        wait = WebDriverWait(driver, 60)

        while True:
            try:
                library_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/libraries/"]')))
                total_links = len(library_links)
                print(f"Found {total_links} library links.")

                if start_index >= total_links:
                    print(f"Start index {start_index} is out of range. Total links: {total_links}")
                    break

                for index in range(start_index - 1, total_links):  # Adjust for 0-based indexing
                    try:
                        library_links = wait.until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/libraries/"]'))
                        )
                        link = library_links[index]

                        print(f"Processing link {index + 1}/{total_links}")
                        link.click()

                        print("Waiting for download link (20 sec timeout)...")

                        try:
                            download_link = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href$=".zip"]'))
                            )
                            download_url = download_link.get_attribute('href')

                            # Use requests to download the file
                            if download_file(download_url):
                                print(f"File downloaded successfully: {download_url}")
                            else:
                                print("Download did not complete successfully.")
                        except TimeoutException:
                            print(f"Download link not found within 20 seconds. Skipping link {index + 1}.")

                        print("Navigating back to main page...")
                        driver.get(website_url)

                        print("Waiting for main page to reload...")
                        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/libraries/"]')))
                        processed_count += 1
                        if processed_count % reset_every == 0:
                            print(f"Resetting WebDriver after {reset_every} links...")
                            driver.quit()
                            driver = initialize_driver()
                            print("WebDriver reset successfully.")

                    except Exception as e:
                        print(f"Error processing link {index + 1}: {e}")
                        traceback.print_exc()

            except Exception as e:
                print(f"Error processing links: {e}")
                traceback.print_exc()

    finally:
        if driver:
            driver.quit()

try:
    process_library_links(start_index=0)
finally:
    print("Downloads complete!")

# Thank You :)