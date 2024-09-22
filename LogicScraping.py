from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import bs4
import pandas as pd
import openpyxl

options = Options()
options.add_experimental_option("detach", True)

#-Install WebDriver everytime it was used-#
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

#-Access the website-#
driver.get("https://www.lazada.co.th/")

#-Find the input field
input_search = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/form/div/div[1]/input[1]")

#-User type what they want to search then enter-#
word = input("Enter what you want to search : ")
input_search.send_keys(word)
input_search.send_keys(Keys.ENTER)

#-Zooming out to see whole page-#
driver.execute_script("document.body.style.zoom = '10%'")

#-Extract HTML page source-#
data = driver.page_source

#-Using Beautiful Soup To find product name-#
soup = bs4.BeautifulSoup(data, features="lxml")
prod_name = soup.find_all("div", {"class": "RfADt"})
all_product = []
for product in prod_name:
    all_product.append(product.text)
#print(all_product)
# print(len(all_product))

#-Using Beautiful Soup To find product price-#
prod_price = soup.find_all("div",{"class":"aBrP0"})
all_price = []
for price in prod_price:
    all_price.append(price.text)
#print(all_price)
# print(len(all_price))

#-Using Beautiful Soup To find product sold amount-#
prod_sold = soup.find_all("span",{"class":"_1cEkb"})
all_sold = []
for sold in prod_sold:
    all_sold.append(sold.text)
#print(all_sold)
# print(len(all_sold))

#-Using Pandas To create dataframe-#
lzd_data = pd.DataFrame({
    "Product Name": all_product,
    "Price":all_price,
    "Amount Sold":all_sold
})
print(lzd_data)

#-Export to Excel-#
#lzd_data.to_excel(r"E:\WebScraping\shopee-เคสไอโฟน.xlsx")
