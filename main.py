from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
from config import *
import datetime
import time

website = "https://www.hotels.com"

def scrape_hotel_prices(location, check_in_date, check_out_date):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(website)

    try:

        # Open Location Search
        location_button = driver.find_element(By.CLASS_NAME, 'button[aria-label="Where to"]')
        location_button.click()

        # Search Location
        location_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "destination_form_field")))
        location_input.clear()
        location_input.send_keys(location)
        location_input.send_keys(Keys.ENTER)

        # Open Calendar
        checkin_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="uitk-date-selector-input1-default"]')))
        checkin_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.uitk-date-display-value')))

        # Validate Date
        check_in_date = datetime.datetime.strptime(check_in_date, "%m-%d-%Y")
        check_out_date = datetime.datetime.strptime(check_out_date, "%m-%d-%Y")
        
        expected_check_in = check_in_date.strftime("%B %Y")
        expected_check_out = check_out_date.strftime("%B %Y")

        # Navigate Calendar
        while True:
            month_year_headers = driver.find_elements(By.CSS_SELECTOR, ".uitk-align-center.uitk-month-label")
            if expected_check_in and expected_check_out in [header.text for header in month_year_headers]:
                break
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-stid="uitk-calendar-navigation-controls-next-button"]')))
                next_month_button = driver.find_element(By.CSS_SELECTOR, 'button[data-stid="uitk-calendar-navigation-controls-next-button"]')
                next_month_button.click()
            except StaleElementReferenceException:
                pass

        # Select Dates
        check_in_date_formatted = check_in_date.strftime("%A, %B %d, %Y")
        check_out_date_formatted = check_out_date.strftime("%A, %B %d, %Y")

        while True:    
            selected_dates = 0        
            try:
                date_buttons = driver.find_elements(By.XPATH, "//td[@class='uitk-day']/div[@class='uitk-day-button uitk-day-selectable uitk-day-clickable']")
                for button in date_buttons:
                    label = button.find_element(By.XPATH, ".//div[@class='uitk-day-aria-label']")
                    aria_label = label.get_attribute("aria-label")
                    if aria_label == "Wednesday 3 April 2024" or aria_label == "Friday 5 April 2024":
                        button.click()
                        selected_dates += 1

                if selected_dates == 2:
                    done_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-stid='apply-date-selector']")))
                    done_button.click()
                    break

            except StaleElementReferenceException:
                pass

        
        # Search
        search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "search_button")))
        search_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".uitk-card-content-section")))
        time.sleep(3)

        # Grab Hotel Elements
        hotel_data = []
        # hotels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between')]")))
        hotels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-primary-theme')]")))
        for hotel in hotels:
            try:
                name_element = hotel.find_element(By.XPATH, ".//h3[contains(@class, 'uitk-heading-5')]")
                hotel_name = name_element.text.strip()

                location_element = hotel.find_element(By.XPATH, ".//div[contains(@class, 'uitk-text')]")
                hotel_location = location_element.text.strip()

                try:
                    price_element = hotel.find_element(By.XPATH, ".//div[contains(@class, 'uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme')]")
                    hotel_price = price_element.text.strip()
                except NoSuchElementException:
                    hotel_price = "SOLD OUT"

                rating_element = hotel.find_element(By.XPATH, ".//span[contains(@class, 'uitk-badge-base-text')]")
                hotel_rating = rating_element.text.strip()

                url_element = hotel.find_element(By.XPATH, ".//a[contains(@class, 'uitk-card-link')]")
                hotel_url = url_element.get_attribute("href")

                hotel_data.append({
                    "Hotel Name": hotel_name,
                    "Location": hotel_location,
                    "Price": hotel_price,
                    "Rating": hotel_rating,
                    "URL": hotel_url
                })

            except Exception as e:
                print(f"Error occurred while extracting hotel data: {e}")

        # Output hotel data
        print(len(hotel_data))
        for hotel in hotel_data:
            print(hotel)

        # Write Hotel Data to Excel
        wb = Workbook()
        ws = wb.active
        ws.append(["Hotel Name", "Location", "Price", "Rating", "URL"])

        for hotel in hotel_data:
            ws.append([hotel["Hotel Name"], hotel["Location"], hotel["Price"], hotel["Rating"], hotel["URL"]])

        wb.save("hotel_data.xlsx")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_hotel_prices(LOCATION, CHECK_IN_DATE, CHECK_OUT_DATE)