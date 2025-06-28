from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

your_name = input("Enter your name: ")

driver = webdriver.Chrome()

# LOGIN
wait_time = 50
driver.get('https://www.linkedin.com/login')

print(f"Please log in manually within {wait_time} seconds...")
for remaining in range(wait_time, 0, -1):
    if remaining % 15 == 0 or remaining <= 10:  # Print every 15s and every second in last 10s
        print(f"{remaining} seconds remaining...")
    time.sleep(1)

print("Time's up!")



# GET CONNECTIONS
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
time.sleep(5)

# Step 4: Scroll to load all connections
print("scrolling to bottom of page...")
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(5)

print("getting connection links...")
elements = driver.find_elements(By.CSS_SELECTOR, 'a.mn-connection-card__picture')
links = [e.get_attribute('href') for e in elements if e.get_attribute('href')]
print("connection links done!")

# Get current timestamp for file naming
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"{your_name}_connections_{timestamp}.txt"

# SAVE CONNECTIONS TO FILE
print("saving connections to file...")
with open(filename, "w") as f:
    for link in links:
        f.write(link + "\n")
        print(link)

driver.quit()
