from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import datetime


def get_position_of_download_element(day, month, year):
    position = 0
    today = datetime.datetime.now()
    input_date = datetime.datetime(year, month, day)
    while today.date() != input_date.date():
        input_date = input_date + datetime.timedelta(days=1)
        if input_date.isoweekday() not in [6, 7]:
            position += 1

    return position


def process_date(input_date):
    day = int(input_date[0:2])
    month = int(input_date[3:5])
    year = int(input_date[6:])
    return day, month, year


def process_input_info(input_date):
    day, month, year = process_date(input_date)
    position_of_download_element = get_position_of_download_element(day, month, year)
    today = str(datetime.datetime.now().date())[0:10]
    splits = today.split('-')
    today = splits[-1] + '/' + splits[-2] + '/' + splits[-3]

    return input_date, today, position_of_download_element


def download_data(input_date, today, position_of_download_element):
    # Set up Chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a UI

    # Set up the Chrome driver

    service = Service('chromedriver-win64/chromedriver.exe')  # Specify the path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the webpage
        driver.get('https://arquivos.b3.com.br/Web/Consolidated')

        waiter = WebDriverWait(driver, 10)
        #clicar na data
        date_picker = waiter.until(
            ec.presence_of_element_located((By.XPATH, f"//div[@class='card-link'][normalize-space()='{input_date}']")))
        date_picker.click()

        date_picker = waiter.until(ec.presence_of_element_located((By.XPATH,
                               f"//div[{position_of_download_element + 1}]//div[5]//div[1]//div[1]//div[1]//div[2]//p[2]//a[1]")))
        date_picker.click()

    except:
        print(
            f'Some error happens while try to download data from "{input_date}"! please check the input and try again!')

        driver.quit()
        return False

    # Close the driver
    time.sleep(1)
    driver.quit()
    return True


def generate_dates(first_date, last_date):
    dates = []
    day, month, year = process_date(first_date)
    date = datetime.datetime(int(year), int(month), int(day)) - datetime.timedelta(days=1)
    last_day, last_month, last_year = process_date(last_date)
    last_date = datetime.datetime(last_year, last_month, last_day)

    while date != last_date:
        date += datetime.timedelta(days=1)
        if date.isoweekday() not in [6, 7]:
            splits = str(date.date())[0:10].split('-')
            day, month, year = splits[-1], splits[-2], splits[-3]
            dates.append(f'{day}/{month}/{year}')

    return dates


if __name__ == '__main__':
    input_init = '28/08/2024'
    input_end = True
    if input_end:
        input_init, input_end = '05/08/2024', '31/08/2024'
        dates = generate_dates(input_init, input_end)
        for d in dates:
            input_date, today, position_of_download_element = process_input_info(d)
            download_data(input_date, today, position_of_download_element)

    else:
        input_date, today, position_of_download_element = process_input_info(input_init)
        download_data(input_date, today, position_of_download_element)
