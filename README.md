# README for Arduino Libraries Downloader

## Overview
This script is designed to automate the downloading of Arduino libraries from the [Arduino Libraries website](https://www.arduinolibraries.info/libraries). It uses Selenium for web scraping and automation, alongside the `requests` library for downloading `.zip` files containing the libraries.

## Features
- Automates the browsing of Arduino library links.
- Downloads `.zip` files directly from the library pages.
- Automatically manages browser sessions with Selenium WebDriver.
- Handles timeouts and retries for downloading files.
- Provides status updates on the downloading process, including file sizes and error handling.

## Requirements
- Python 3.x
- Selenium
- Chrome WebDriver
- Requests library

### Python Libraries
Ensure the following Python packages are installed:
```bash
pip install selenium requests
```

### WebDriver Setup
Download the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and update the `driver_path` in the script to match your system path.

```python
driver_path = 'C:/chromedriver.exe'
```

## Installation and Usage

1. **Download or clone the repository:**

   ```bash
   git clone https://github.com/your-repo/arduino-downloader.git
   cd arduino-downloader
   ```

2. **Set up download folder:**

   Modify the `download_folder` in the script to point to where you want the `.zip` files to be downloaded:

   ```python
   download_folder = 'C:/Arduino_Files'
   ```

3. **Run the script:**

   ```bash
   python arduino_downloader.py
   ```

   The script will open a browser window, visit the Arduino Libraries page, and start downloading the library files automatically. Each file's download status will be printed in the console.

## Script Details

### Core Functions:

- **`initialize_driver()`**: Initializes the Chrome WebDriver and opens the Arduino Libraries website.
  
- **`process_library_links(start_index=0, reset_every=100)`**: Processes and iterates through all library links on the webpage. Downloads the libraries in `.zip` format, and resets the WebDriver every 100 downloads to maintain stability.

- **`download_file(download_link)`**: Uses the `requests` library to download the file at the provided link and saves it to the specified download folder.

- **`wait_for_download(download_folder, timeout=20)`**: Waits for a file to be completely downloaded by monitoring the download folder.

### Error Handling:

- The script logs errors if a link cannot be processed, providing stack traces via the `traceback` module.
- Handles timeouts when a download link is not found within 20 seconds.

## Customization

- **Start Index**: If you wish to resume downloading from a specific index of the library links, adjust the `start_index` parameter in the `process_library_links` function.
  
- **Reset Frequency**: By default, the WebDriver is reset every 100 downloads. You can adjust this by modifying the `reset_every` parameter.

## Disclaimer
This script is for educational purposes. Ensure you comply with the terms of use of the Arduino Libraries website when using this script. 

---

**#Made by Mesbah (Lamp)**
