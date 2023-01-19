from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import pandas as pd
import os
from pathlib import Path
import time



def input_last_name(browser, last_name_key):
    last_name_input = browser.find_element(By.XPATH, '//*[@id="t_web_lookup__last_name"]')
    last_name_input.send_keys(last_name_key)
    
    return print(f'\tLast Name: {last_name_key}\n')


def input_license_type(browser, license_type):
    if license_type == 1:
        return print(f'\n\tLicense Type: All\n')
    if license_type != 1:
        browser.find_element(By.XPATH, '//*[@id="t_web_lookup__license_type_name"]').click()
        license_type_input = browser.find_element(By.XPATH, 
                             f'/html/body/form/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[3]/td/span/fieldset/table/tbody/tr[2]/td[2]/select/option[{license_type}]')
        lt_text = license_type_input.get_attribute('value')
        license_type_input.click()
        return print(f'\n\tLicense Type: {lt_text}\n')


def save_csv_to_extraction(workdir, dict_var, last_name, license_type):
    with open(os.path.join(f'{workdir}/extraction', f"idbop_last-name-{last_name}_license-type-{license_type}.csv"), 'wb') as f:
        df = pd.DataFrame(dict_var)
        
        return df.to_csv(f, index=False, header=True)
    

def check_max_pages(browser):
    # Not applicable for less than 40 a tags
    try:
        
        pg_check_count = 0
        pg_check = True
        # import pdb; pdb.set_trace()
        while pg_check:
            last_item = browser.find_elements(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td/table/tbody/tr[42]/td/a')[-1]
            if last_item.text == '...':
                last_item.click()
                time.sleep(5)
                pg_check_count += 1
            else:
                pg_nb = last_item.text
                pg_check = False

    except NoSuchElementException:
        pg_nb = browser.find_elements(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td/table/tbody/tr[42]/td/a')[-1].text
    
    for i in range(pg_check_count):
        browser.back()
    
    return int(pg_nb)