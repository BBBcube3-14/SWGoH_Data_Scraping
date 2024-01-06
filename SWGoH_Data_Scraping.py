from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from selenium.common.exceptions import TimeoutException

def printData(user_data):
    maxLvl = 0
    eighty = 0
    seventy = 0
    sixty = 0
    fifty = 0
    less = 0
    seven = 0
    six = 0
    five = 0
    four = 0
    three = 0
    two = 0
    one = 0
    for data in user_data:
        if data[2] == 85:
            maxLvl += 1
        elif data[2] >= 80:
            eighty += 1
        elif data[2] >= 70:
            seventy += 1
        elif data[2] >= 60:
            sixty += 1
        elif data[2] >= 50:
            fifty += 1
        else:
            less += 1

        if(data[1] == 7):
            seven += 1
        elif(data[1] == 6):
            six += 1
        elif(data[1] == 5):
            five += 1
        elif(data[1] == 4):
            four += 1
        elif(data[1] == 3):
            three += 1
        elif(data[1] == 2):
            two += 1
        else:
            one += 1    
    print("Levels:")
    print("85:", maxLvl)
    print("80:", eighty)
    print("70:", seventy)
    print("60:", sixty)
    print("50:", fifty)
    print("<50:", less)
    print("Stars")
    print("7*", seven)
    print("6*", six)
    print("5*", five)
    print("4*", four)
    print("3*", three)
    print("2*", two)
    print("1*", one)

def extract_character_data(driver):
    try:
        # Add a general wait for page to load
        driver.implicitly_wait(10)

        # Now use WebDriverWait with a longer timeout
        wait = WebDriverWait(driver, 20)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        character_entries = soup.select('.collection-char-list .collection-char')

        character_data = []

        for character_entry in character_entries:
            character_name = character_entry.select_one('.collection-char-name-link').get_text(strip=True)

            relic_element = character_entry.select_one('.character-portrait__relic--size-normal')
            if relic_element:
                character_level = 85
            else:
                level_element = character_entry.select_one('.character-portrait__level--size-normal')
                if level_element:
                    character_level = int(level_element.get_text(strip=True))
                else:
                    character_level = None

            total_stars = 7  # assuming 7 stars as default
            active_stars = len(character_entry.select('.character-portrait__star--size-normal:not(.character-portrait__star--inactive)'))
            if active_stars < total_stars:
                total_stars = active_stars

            character_data.append([character_name, active_stars, character_level])

        return character_data

    except TimeoutException:
        print("Timeout: Unable to extract character data.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None















def extract_ship_data(driver):
    try:
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ship_entries = soup.select('.collection-char-list .collection-ship')
        ship_data = []
        for ship_entry in ship_entries:
            ship_name = ship_entry.select_one('.collection-ship-name-link').get_text(strip=True)
            
            level_element = ship_entry.select_one('.ship-portrait__level--size-normal')
            if level_element:
                ship_level = int(level_element.get_text(strip=True))
            else:
                ship_level = None
            total_stars = 7  # assuming 7 stars as default
            active_stars = len(ship_entry.select('.ship-portrait__star--size-normal:not(.ship-portrait__star--inactive)'))
            if active_stars < total_stars:
                total_stars = active_stars
            ship_data.append([ship_name, active_stars, ship_level])
        return ship_data
    except TimeoutException:
        print("Timeout: Unable to extract ship data.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None













ally_code = input("Enter your allycode:")
url_to_scrape = 'https://swgoh.gg/p/'+ally_code+'/characters/'
#Add your ally code here ----------------------^
csv_output_file = 'ship_data.csv'

# Use Safari driver
driver = webdriver.Safari()
driver.get(url_to_scrape)

# Extract Galactic Power and ship Data
ship_data = extract_character_data(driver)

# Save the data to a CSV file
if ship_data is not None:
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['ship Name', 'Active Stars', 'ship Level'])
        w.writerows(ship_data)

    
print(f"Data saved to {csv_output_file}")
star_track = sum(data[2] for data in ship_data)
print("Total Stars:", star_track)
printData(ship_data)
driver.quit()

url_to_scrape = 'https://swgoh.gg/p/'+ally_code+'/ships/'
# #Add your ally code here ----------------------^
csv_output_file = 'ship_data.csv'

# # Use Safari driver
driver = webdriver.Safari()
driver.get(url_to_scrape)

# Extract Galactic Power and ship Data
ship_data = extract_ship_data(driver)

# Save the data to a CSV file
if ship_data is not None:
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Ship Name', 'Active Stars', 'Ship Level'])
        w.writerows(ship_data)

    
print(f"Data saved to {csv_output_file}")
star_track = sum(data[2] for data in ship_data)
print("Total Stars:", star_track)
printData(ship_data)
driver.quit()