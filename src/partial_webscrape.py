from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sessions_status_updater
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Set Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode (background running)

# Initialize the Chrome driver with the configured options
driver = webdriver.Chrome(options=chrome_options)

def press_button(button):
    wait = WebDriverWait(driver, 30)
    key_word_button=wait.until(EC.visibility_of_element_located(button))
    key_word_button.click()

driver.get("https://sis.rutgers.edu/soc/#subjects?semester=92023&campus=NB&level=U")
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 30)
press_button((By.ID, "keyword_search_id"))

course_search = driver.find_element(By.ID, "keyword_textbox_id")
with open(os.getenv('COURSE_NUMBERS_TXT'),'r') as f:
    search_query = f.read().splitlines()
print(search_query)
elements=[]
course_dictionary = dict()
for course_number in search_query:
    course_search.send_keys(course_number)
    press_button((By.ID,'keywordSubmit'))
    press_button((By.ID,f'courseId.{course_number}'))

    section_elements = driver.find_elements(By.CLASS_NAME, "sectionIndexNumber")
    section_numbers= [ele.text for ele in section_elements]

    course_dictionary[str(course_number)] = section_numbers
    elements.append(section_numbers)
    course_search.clear()
    driver.implicitly_wait(10)

with open(os.getenv('INDEX_FILE_TXT'), mode='w') as f:
    for section_numbers in elements:
        for number in section_numbers:
            f.write(number + '\n')


#sessions_status_updater.main()
