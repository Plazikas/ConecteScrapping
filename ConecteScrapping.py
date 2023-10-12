from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Definition variables what initialize firefox
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
firefox_driver = '/usr/local/bin/geckodriver'
firefox_service = Service(firefox_driver)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)
conecte_website = 'https://www.conecte.es/index.php/es/plantas/mapa'

# IInitialize firefox browser
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
driver.get(conecte_website)

wait = WebDriverWait(driver, 10)

# Selecting the province
province_option_almeria = '/html/body/div[1]/div/div/div/main/form/div[1]/div[1]/div[2]/select/option[4]'
province_option_navarra = '/html/body/div[1]/div/div/div/main/form/div[1]/div[1]/div[2]/select/option[36]'

wait.until(EC.presence_of_element_located((By.XPATH, province_option_navarra)))
province_botton = wait.until(EC.element_to_be_clickable((By.XPATH, province_option_navarra)))
province_botton.click()

apply_filter = '/html/body/div[1]/div/div/div/main/form/div[1]/div[3]/div/div/button[1]'
wait.until(EC.presence_of_element_located((By.XPATH, apply_filter)))
apply_filter_botton = wait.until(EC.element_to_be_clickable((By.XPATH, apply_filter)))
apply_filter_botton.click()

# Visualize 100 entries max
n_entries = '/html/body/div[1]/div/div/div/main/form/div[5]/div[2]/select/option[4]'
wait.until(EC.presence_of_element_located((By.XPATH, n_entries)))
n_entries_botton = wait.until(EC.element_to_be_clickable((By.XPATH, n_entries)))
n_entries_botton.click()

# Take municipalities information one by one
municipality_name_list = []
comarca_list = []
file_date_list = []
file_user_list = []
file_name_list = []
file_type_list = []
file_content_list = []

municipalities = driver.find_elements(By.CSS_SELECTOR, 'tr')
for municipality_row in municipalities:
    
    n_files_found = 0
    
    municipality_data = municipality_row.find_elements(By.CSS_SELECTOR, 'td')
    if len(municipality_data) == 5:
        municipality_name = municipality_data[0].text
        comarca = municipality_data[1].text
        province = municipality_data[2].text
        autonomous_community = municipality_data[3].text
        n_infos = int(municipality_data[4].text)

        # print(municipality_name, comarca, province, autonomous_community, n_infos)

        municipality_link = municipality_data[0].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        
        # Open the link for each municipality
        municipality_service = Service(firefox_driver)
        municipality_driver = webdriver.Firefox(service=municipality_service, options=firefox_options)
        municipality_driver.get(municipality_link)
        wait_municipality = WebDriverWait(municipality_driver, 10)

        # Show 100 files per page if necessary
        n_pages = int(n_infos / 100) + 1

        if n_infos > 20:
            n_files_show = '/html/body/div[1]/div/div/div/main/form/div[4]/div[1]/select/option[8]'
            wait_municipality.until(EC.presence_of_element_located((By.XPATH, n_files_show)))
            n_files_show_botton = wait_municipality.until(EC.element_to_be_clickable((By.XPATH, n_files_show)))
            n_files_show_botton.click()

        # Take the info of each file and add to the list
        for i in range (n_pages):
            info_table = '/html/body/div[1]/div/div/div/main/form/table/tbody'
            wait_municipality.until(EC.presence_of_element_located((By.XPATH, info_table)))
            file_entries = municipality_driver.find_elements(By.CSS_SELECTOR, 'tr')
            for file_row in file_entries:
                file_data = file_row.find_elements(By.CSS_SELECTOR, 'td')
                if len(file_data) == 6:
                    municipality_name_list.append(municipality_name)
                    comarca_list.append(comarca)
                    file_date_list.append(file_data[0].text)
                    file_user_list.append(file_data[1].text)
                    file_name_list.append(file_data[2].text)
                    file_type_list.append(file_data[3].text)
                    file_content_list.append(file_data[4].text)
                    
                    n_files_found += 1

            # Go to the next page if necessary
            if n_pages > 1 and i < (n_pages - 1):
                if n_pages < 10:
                    next_page = municipality_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/form/table/tfoot/tr/td/div/ul/li[' + str(i + 4) + ']/a')
                else:
                     next_page = municipality_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/form/table/tfoot/tr/td/div/ul/li[13]/a/span')
                pagination = municipality_driver.find_element(By.CLASS_NAME, 'pagination')
                municipality_driver.execute_script("arguments[0].click();", next_page)
                time.sleep(5)

        municipality_driver.quit()

driver.quit()

# Create dataframe with info files and export to excel 
data_files = {'Municipality': municipality_name_list, 'Comarca': comarca_list, 'Date': file_date_list, 'User': file_user_list, 'File': file_name_list, 'Type': file_type_list, 'Content': file_content_list}
df = pd.DataFrame(data_files)
df.to_excel('Escritorio/ConecteScrapping/ConecteDataNavarra2.xlsx', index = False)

print('END')