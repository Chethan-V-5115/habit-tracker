from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000")

# Example: tick the first habit
checkbox = driver.find_elements(By.TAG_NAME, "input")[0]
checkbox.click()
time.sleep(2)

print("Test complete: Habit ticked.")
driver.quit()
