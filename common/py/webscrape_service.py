# jinka/common/py/webscrape_service.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from common.py.webscrape_connection import get_driver
import csv
from datetime import datetime


def perform_search_with_selenium(url, search_term=None):
    driver = get_driver()
    driver.get(url)

    if search_term:
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'searchTerm'))
        )
        search_input.send_keys(search_term)
        search_button = driver.find_element(By.ID, 'searchButton')
        search_button.click()
        time.sleep(10)

    html_content = driver.page_source
    driver.quit()
    return html_content


def scrape_and_parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first available table or a table with a specific ID
    table = soup.find('table', {'id': 'businessSummaryTable'}) or soup.find('table')

    if not table:
        return [], []

    # Extract headers
    thead = table.find('thead')
    headers = [header.text.strip() for header in thead.find_all('th')] if thead else []

    # Extract data rows
    tbody = table.find('tbody')
    data = []
    if tbody:
        for row in tbody.find_all('tr'):
            row_data = {headers[i]: col.text.strip() for i, col in enumerate(row.find_all('td'))} if headers else [
                col.text.strip() for col in row.find_all('td')]
            data.append(row_data)
    return headers, data


def save_data_to_csv(headers, data, csv_filename="output.csv"):
    if not csv_filename:
        # Use a timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"scraped_data_{timestamp}.csv"

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers) if headers else csv.writer(file)
        if headers:
            writer.writeheader()
        writer.writerows(data)

    return csv_filename
