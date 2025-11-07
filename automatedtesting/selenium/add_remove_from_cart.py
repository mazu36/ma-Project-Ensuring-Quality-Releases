# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


# Start the browser and login with standard_user
def login (user, password):

  try:
    logging.info('Starting the browser...')
    #driver = webdriver.Chrome()  # MDE: when launched locally  
    
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    #options.add_argument("--remote-debugging-port=9222")
    
    driver = webdriver.Chrome(options=options)

    demo_web_page='https://www.saucedemo.com/'
    logging.info(f"Browser started successfully. Navigating to the demo page {demo_web_page} to login.")
    driver.get(demo_web_page) 
    logging.info(f"Connected to the demo page {demo_web_page} successfully.")

    logging.info(f"Connecting of the user {user}:")
    driver.find_element(By.ID, 'user-name').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()
    logging.info(f"Connected the user {user} successfully")
    return (0, driver)
  except RuntimeError as e:
    logging.info(f"Error {e} on login of the user {user}")
    return (1,driver)

# --------------------------------------------------------
# 
#                          M A I N
# 
# --------------------------------------------------------
(cr, driver)=login('standard_user', 'secret_sauce')
if cr != 0:
  exit

driver.implicitly_wait(2)


# functional UI tests as per your requirements. 
# UI Test 1: adds all products to a cart, 
# UI Test 2: removes all products from a cart.

logging.info("Retrieving shopping cart icon:")
cart_icon = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
logging.info("Shopping cart icon is retrieved successfully")


time.sleep(5)  # Wait for 5 seconds

#  --- Test 1 ---
logging.info("*** UI Test 1: adding all products to a cart***")
# Find all <button> elements with an 'id' attribute whose id starts with 'add-to-cart'
buttons_add = driver.find_elements(By.CSS_SELECTOR, "button[id^='add-to-cart']")

# Extract button IDs into a Python list
buttons_ids = [button.get_attribute("id") for button in buttons_add]
logging.info(f"Buttons 'add-to-cart' are: {buttons_ids}")


#driver.implicitly_wait(2)
time.sleep(20)  # Wait for 20 seconds 

nb_item_added=0
for idx, button_id in enumerate(buttons_ids): 
  driver.find_element(By.ID, button_id).click() 
  logging.info(f"Item {idx+1} added successfully:  button_id {button_id}") 
  nb_item_added +=1


#  --- Test 2 ---
time.sleep(40)  # Wait for 40 seconds
logging.info("*** UI Test 2: removing all products from a cart***")
# Find all <button> elements with an 'id' attribute whose id starts with 'add-to-cart'
buttons_rm = driver.find_elements(By.CSS_SELECTOR, "button[id^='remove']")

# Extract button IDs into a Python list
buttons_ids = [button.get_attribute("id") for button in buttons_rm]
logging.info(f"Buttons 'remove' are: {buttons_ids}")


nb_item_removed=0
for idx, button_id in enumerate(buttons_ids):
  driver.find_element(By.ID, button_id).click()
  logging.info(f"Item {idx+1} removed successfully:  button_id {button_id}") 
  nb_item_removed +=1


logging.info(f"Number of items added   into the cart: {nb_item_added} item(s)")
logging.info(f"Number of items removed from the cart: {nb_item_removed} item(s)")


time.sleep(5)  # Wait for 5 seconds

driver.quit()








