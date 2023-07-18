#Only run this for auto scheduling
#Probably takes a lot of time

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

load_dotenv


def main():
    with open(os.getenv('COURSE_DICTIONARY'), 'r') as f:
        course_dictionary = json.load(f)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode (background running)
    driver = webdriver.Chrome(options=chrome_options)

    def press_button(button):   #press button method so i dont have to run click everytime
        wait = WebDriverWait(driver, 30)
        key_word_button=wait.until(EC.visibility_of_element_located(button))
        key_word_button.click()

    driver.get("https://sis.rutgers.edu/soc/#subjects?semester=92023&campus=NB&level=U")    #Opens this webpage 
    driver.implicitly_wait(5)   #wait for 5 seconds for the page to load so it doesn't time out

    press_button((By.ID, "keyword_search_id"))

    course_search = driver.find_element(By.ID, "keyword_textbox_id")
    with open(os.getenv('COURSE_NUMBERS_TXT'),'r') as f:
        search_query = f.read().splitlines()

    for course_number in search_query:  #for each course number in the file course_numbers.txt we will enter each into seach bar and get info

        print(f"Starting identifying course {course_number}")   #logger

        if not dictionary_check(course_dictionary,course_number):   #checks if it has already been searched to save resources
            course_dictionary[course_number] = dict()

        course_search.send_keys(course_number)  #this enters the course number
        press_button((By.ID,'keywordSubmit'))
        press_button((By.ID,f'courseId.{course_number}'))   #just here u can see how important the press button method is.


        section_div = driver.find_elements(By.ID, f"{course_number}.0.sectionListings")
        i = 1
        while len(section_div) < 1:
            section_div = driver.find_elements(By.ID, f"{course_number}.{i}.sectionListings")
            i+=1
        section_listings = section_div[0].find_elements(By.XPATH,"./div[contains(@class, 'sectionStatus')]")
        
        print("Starting webscrape....")

        for ele in section_listings:    #this loop checks the course and gets all the index number, section notes, etc.
            index=""
            restrictions=""
            day=[]
            time=[]
            campus=[]


            section_index = ele.find_elements(By.CLASS_NAME, "sectionIndexNumber")
            if(len(section_index)!=0):
                index = section_index[0].text
            if dictionary_check(course_dictionary,index):
                print(f"index {index} already exists, skipping...")
                continue
             
            section_restrictions = ele.find_elements(By.CLASS_NAME,"sectionNotes")
            if(len(section_restrictions)!=0):
                restrictions=section_restrictions[0].text
            section_data = ele.find_elements(By.CLASS_NAME, "sectionMeetingTimesDiv")
            section_data_inner=section_data[0].find_elements(By.XPATH,".//*")

            course_dictionary[course_number][index]=dict()
            class_count = 0
            for txt in section_data_inner:
                if ' ' in txt.text:
                    class_count+=1
                    course_dictionary[course_number][index][f"Class{class_count}"]=dict()
                    for dt in txt.find_elements(By.XPATH,".//*"):
                        dt = dt.text
                        if ':' in dt:
                            time.append(dt)
                            course_dictionary[course_number][index][f"Class{class_count}"]["Time"] = dt
                        elif 'day' in dt:
                            day.append(dt)
                            course_dictionary[course_number][index][f"Class{class_count}"]["Day"] = dt
                        else:
                            campus.append(dt)
                            course_dictionary[course_number][index][f"Class{class_count}"]["Campus and Classroom"] = dt
                            break
                    if len(course_dictionary[course_number][index][f"Class{class_count}"]) == 0:
                        del course_dictionary[course_number][index][f"Class{class_count}"]
                        class_count-=1
            course_dictionary[course_number][index]['restrictions']=str(restrictions)
            print(f"We are done with index #{index}")
            
        
        course_search.clear()
        driver.implicitly_wait(10)  #to make sure it doesn't time out
    print("**********process complete**********")

    with open(os.getenv('COURSE_DICTIONARY'), 'a') as f:
        json.dump(course_dictionary,f, indent=4)    #dumps the final dict to json so its easier to see.

def dictionary_check(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return True
        elif key == value:
            return True
        elif isinstance(val, dict):
            if dictionary_check(val, value):
                return True
    return False


##################
main()