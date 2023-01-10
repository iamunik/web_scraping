from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

# Selecting the number of pages you want to scrape
page_no = int(input("How many pages do you wish to scrape?\n-> "))

while page_no > 20:
    page_no = int(input("Page number selected is greater than pages existing\nTotal pages is 20\n"
                        "How many pages do you wish to scrape?\n-> "))

# Setting the driver object
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("http://books.toscrape.com/")
title = driver.title

print(title)

# Empty lists to populate the dataframe
bookTitle = []
price = []
stock_status = []
description = []
category = []
upc = []
productType = []
price_iTax = []
price_eTax = []
tax = []
numberOfReview = []

c_i = 0  # counter item
c_p = 0  # counter page

while c_p != page_no:
    for i in driver.find_elements(By.TAG_NAME, 'h3'):
        c = driver.find_element(By.LINK_TEXT, i.text)
        c.click()

        book_title = driver.find_element(By.CLASS_NAME, 'active').text
        bookTitle.append(book_title)

        pric_e = driver.find_element(By.CLASS_NAME, 'price_color').text
        price.append(pric_e)

        cat = driver.find_elements(By.TAG_NAME, 'a')
        cats = [i.text for i in cat]
        category.append(cats[3])

        inStock = driver.find_element(By.CLASS_NAME, 'instock').text
        stock_status.append(inStock)

        p_i = driver.find_elements(By.TAG_NAME, 'td')
        product_info = [i.text for i in p_i]
        upc.append(product_info[0])
        productType.append(product_info[1])
        price_eTax.append(product_info[2])
        price_iTax.append(product_info[3])
        tax.append(product_info[4])
        numberOfReview.append(product_info[6])

        p_d = driver.find_elements(By.TAG_NAME, 'p')
        pro_d = [i.text for i in p_d]
        description.append(pro_d[3])

        driver.back()
        c_i += 1

        if c_i == 20:
            c_i = 0
            cc = driver.find_elements(By.TAG_NAME, 'a')
            ac = [i.text for i in cc]
            driver.find_element(By.LINK_TEXT, ac[93]).click()
    c_p += 1

driver.close()

data = {
    "book_title": bookTitle,
    "category": category,
    "price": price,
    "UPC": upc,
    "stock_status": stock_status,
    "description": description,
    "product_type": productType,
    "tax": tax,
    "price_incl_tax": price_iTax,
    "price_excl_tax": price_eTax,
    "number_of_review": numberOfReview
}

booksToScrape = pd.DataFrame(data)

print(booksToScrape)

name_file = input("\nPLEASE NOTE!!\nEnter just the filename without the file extension\n"
                  "Enter a preferred file name:\n-> ")

if ".csv" in name_file:
    name_file = name_file[:-4]

name_of_file = str(name_file + ".csv")

booksToScrape.to_csv(name_of_file, index=False)
print(f"{name_of_file} saved to Directory")
