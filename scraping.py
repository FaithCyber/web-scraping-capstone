from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

url = "https://www.timeanddate.com/weather/"  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

time.sleep(3)

data = []

items = driver.find_elements(By.TAG_NAME, "div")

for item in items:
    try:
        data.append({"text": item.text})
    except:
        pass

driver.quit()

df = pd.DataFrame(data)
df.to_csv("data/raw_data.csv", index=False)

print("Scraping complete!")