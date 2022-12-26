from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

quotes_no = int(input("How many quotes do you wish to scrape?\n-> "))

while quotes_no > 90:
    quotes_no = int(input("Quotes requested for is greater than the available amounts of quotes existing\n"
                          "Total quotes is 90\nHow many quotes do you wish to scrape?\n-> "))

driver.get("http://quotes.toscrape.com/")
title = driver.title

print(title)

quotes = []
author = []
dateOfBirth = []
description = []
location = []

c_p = 1
while c_p != quotes_no:
    for i in driver.find_elements(By.CLASS_NAME, 'text'):
        quotes.append(i.text)
    for i in driver.find_elements(By.LINK_TEXT, '(about)'):
        i.click()
        auth = driver.find_element(By.CLASS_NAME, 'author-title').text
        author.append(auth)
        dob = driver.find_element(By.CLASS_NAME, 'author-born-date').text
        dateOfBirth.append(dob)
        locatn = driver.find_element(By.CLASS_NAME, 'author-born-location').text
        location.append(locatn[3:])
        desc = driver.find_element(By.CLASS_NAME, 'author-description').text
        description.append(desc)
        driver.back()
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Next ').click()
    if c_p == quotes_no:
        break
    c_p += 1

driver.close()

data = {
    'Author': author,
    "DateOfBirth": dateOfBirth,
    "Location": location,
    "Quotes": quotes,
    "Description": description
}

quotesToScrape = pd.DataFrame(data)

print(data)

name_file = input("\nPlease note enter just the filename without the file extension\nEnter a preferred file name:\n-> ")

name_of_file = str(name_file + ".csv")

quotesToScrape.to_csv(name_of_file, index=False)
