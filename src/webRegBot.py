from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

credentials = {
    'username': '', #username password for login
    'password': '',
}
print("amongus")
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=")
chrome_options.add_argument(r'--profile-directory=Profile 1')
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)


browser.get('https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection=92019&indexList=00000')

usernameBox = browser.find_element(By.ID, 'username')
usernameBox.send_keys(credentials['username'])
passwordBox = browser.find_element(By.ID, 'password')
passwordBox.send_keys(credentials['password'])
submitButton = browser.find_element(By.NAME, 'submit')
submitButton.click()

# Wait for the login process to complete (adjust the sleep time as needed)
sleep(10)

# Further actions or automation can be added here

# Close the browser
