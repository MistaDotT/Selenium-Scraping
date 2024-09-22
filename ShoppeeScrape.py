from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def configure_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def search_product(driver, search_term):
    driver.get("https://www.lazada.co.th/")
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search in Lazada']"))
    )
    search_input.send_keys(search_term + Keys.ENTER)

def extract_product_data(soup):
    product_names = [product.text for product in soup.find_all("div", class_="RfADt")]
    product_prices = [price.text for price in soup.find_all("div", class_="aBrP0")]
    products_sold = [sold.text for sold in soup.find_all("span", class_="_1cEkb")]
    product_origins = [origin.text for origin in soup.find_all("span", class_="oa6ri")]
    
    return list(zip(product_names, product_prices, products_sold, product_origins))

def scrape_multiple_pages(driver, num_pages=5):
    all_products = []
    
    for _ in range(num_pages):
        driver.execute_script("document.body.style.zoom = '10%'")
        time.sleep(2)  # Wait for the page to load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        all_products.extend(extract_product_data(soup))
        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='ant-pagination-next']/button"))
            )
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except:
            print("No more pages to scrape or reached the limit.")
            break
    
    return all_products

def main():
    driver = configure_driver()
    search_term = input("Enter what you want to search: ")
    search_product(driver, search_term)
    
    all_products = scrape_multiple_pages(driver)
    
    lzd_data = pd.DataFrame(all_products, columns=["Product Name", "Price", "Amount Sold", "Origin"])
    print(lzd_data)
    
    # Uncomment the line below to export to Excel
    lzd_data.to_excel(r"E:\WebScraping\lazada_products.xlsx", index=False)
    
    driver.quit()

if __name__ == "__main__":
    main()