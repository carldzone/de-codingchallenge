from selenium.webdriver.common.by import By
import pandas as pd
import os
from pathlib import Path



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