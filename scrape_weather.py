from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

url = "https://www.timeanddate.com/weather/"
driver.get(url)

time.sleep(3)

cities = []
temps = []

try:
    rows = driver.find_elements(By.CSS_SELECTOR, "table.zebra.tb-wt tbody tr")

    for row in rows:
        try:
            city = row.find_element(By.TAG_NAME, "th").text
            temp = row.find_element(By.TAG_NAME, "td").text

            cities.append(city)
            temps.append(temp)

        except:
            pass

except Exception as e:
    print(e)

driver.quit()

df = pd.DataFrame({
    "City": cities,
    "Temperature": temps
})

print(df.head())

df.to_csv("weather_data_raw.csv", index=False)

print("Raw CSV saved.")