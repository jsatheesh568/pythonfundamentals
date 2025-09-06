from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/")

element = driver.find_element(By.ID, "content")
element = driver.find_element(By.LINK_TEXT, "A/B Testing")
element = driver.find_element(By.XPATH, '//*[@id="content"]/ul/li[1]/a')

#WAIT
wait = WebDriverWait(driver, 10)
element= wait.until(EC.presence_of_element_located((By.ID, "content")))
driver.implicitly_wait(10) # seconds    







