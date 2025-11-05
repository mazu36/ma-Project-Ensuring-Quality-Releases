# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time


# Start the browser and login with standard_user
def login (user, password):

  try:
    print ('Starting the browser...')
    
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    #options.add_argument("--remote-debugging-port=9222")
    
    driver = webdriver.Chrome(options=options)

    #driver = webdriver.Chrome()  # MDE
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    print(f"Connection of the user {user}:")
    driver.find_element(By.ID, 'user-name').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()
    print(f"Connection of the user {user} is processed successfully")
    return (0, driver)
  except RuntimeError as e:
    print(f"Error {e} on login of the user {user}")
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

print("Retrieving shopping cart icon:")
cart_icon = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
print("Shopping cart icon is retrieved successfully")
cart_item_count = cart_icon.text
print(f"Initial Number of items in the cart: {cart_item_count} item(s)")




time.sleep(5)  # Wait for 5 seconds

#  --- Test 1 ---
print("*** UI Test 1: adding all products to a cart***")
# Find all <button> elements with an 'id' attribute whose id starts with 'add-to-cart'
buttons_add = driver.find_elements(By.CSS_SELECTOR, "button[id^='add-to-cart']")

# Extract button IDs into a Python list
buttons_ids = [button.get_attribute("id") for button in buttons_add]
print(f"Buttons 'add-to-cart' are: {buttons_ids}")


driver.implicitly_wait(20)

time.sleep(40)  # Wait for 40 seconds
#time.sleep(40)  # Wait for 40 seconds

for idx, button_id in enumerate(buttons_ids): 
  driver.find_element(By.ID, button_id).click() 
  cart_item_count = cart_icon.text
  print(f"Step {idx} Adding: Number of items in the cart: {cart_item_count} button_id  {button_id}") 

cart_item_count = cart_icon.text
print(f"Final number of items in the cart after adding all products: {cart_item_count} item(s)")


#  --- Test 2 ---
print("*** UI Test 2: removing all products from a cart***")
# Find all <button> elements with an 'id' attribute whose id starts with 'add-to-cart'
buttons_rm = driver.find_elements(By.CSS_SELECTOR, "button[id^='remove']")

# Extract button IDs into a Python list
buttons_ids = [button.get_attribute("id") for button in buttons_rm]
print(f"Buttons 'remove' are: {buttons_ids}")
for idx, button_id in enumerate(buttons_ids):
  driver.find_element(By.ID, button_id).click()
  cart_item_count = cart_icon.text
  print(f"Step {idx} Removing: Number of items in the cart: {cart_item_count}")

cart_item_count = cart_icon.text 
print(f"Final number of items in the cart after removing all products: {cart_item_count} item(s)")


time.sleep(5)  # Wait for 5 seconds

driver.quit()




