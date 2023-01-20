from function import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import sys
import argparse

def main(params):
    
    ln = params.ln
    lt = params.lt
    
    t = time.time()
    cwd = os.getcwd()
    
    data_content = {
        'First Name': [], 'Middle Name': [], 'Last Name': [], 'License Number': [],
        'License Type': [], 'Status': [], 'Original Issued Date': [], 'Expiry': [],
        'Renewed': []
    }
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    
    url = 'https://idbop.mylicense.com/verification/Search.aspx'
    browser.get(url)
    time.sleep(5)
    
    # Using input_last_name and input_license_type function to search for ID's
    try:
        input_last_name(browser, ln)
    except NameError:
        print(f'\tLast Name "{ln}" is an invalid input')
        browser.quit()
        sys.exit()
    input_license_type(browser, lt)
    # Searching for inputs
    browser.find_element(By.XPATH, '//*[@id="sch_button"]').click()
    time.sleep(5)
    
    # Checking the maximum pages to extract data
    pg_nb = check_max_pages(browser)
    
    print(f'\n\tTotal number of pages to check: {str(pg_nb)}\n')
    pg_counter = 0
    pg_row = 0
    for pg in range(pg_nb):
        pg_counter += 1
        print(f'\n\tChecking data from page {pg_counter + pg_row}\n')
        # Get every row information from Result and getting each item's LINK
        links = [elmt.get_attribute('href') for elmt in browser.find_elements(By.XPATH, '//*[@id="datagrid_results"]/tbody/tr/td[1]/table/tbody/tr/td[1]/a')]
        
        print(f'\tTotal number of rows to check: {len(links)}\n')
        for i in range(len(links)):
            link = links[i]
            try:
                browser.get(link)
            except WebDriverException:
                reload_page_extraction(browser, url, link, ln, lt, pg)
            
            last_name = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td/span/table/tbody/tr/td/table/tbody/tr[1]/td[8]').text
            first_name = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td/span/table/tbody/tr/td/table/tbody/tr[1]/td[4]').text
            middle_name = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td/span/table/tbody/tr/td/table/tbody/tr[1]/td[6]').text
            license_nb = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[2]/td[2]').text
            license_type = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[2]/td[4]').text
            status = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[3]/td[2]').text
            orig_issued_date = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[3]/td[4]').text
            expiry = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[3]/td[6]').text
            renewed = browser.find_element(By.XPATH, '//*[@id="TheForm"]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr[10]/td/span/table/tbody/tr/td/table/tbody/tr[4]/td[6]').text

            print(last_name)
            print(first_name)
            print(middle_name)
            print(license_nb)
            print(license_type)
            print(status)
            print(orig_issued_date)
            print(expiry)
            print(renewed)
            print(link)
            print('\n\n')
            data_content['First Name'].append(first_name)
            data_content['Middle Name'].append(middle_name)
            data_content['Last Name'].append(last_name)
            data_content['License Number'].append(license_nb)
            data_content['License Type'].append(license_type)
            data_content['Status'].append(status)
            data_content['Original Issued Date'].append(orig_issued_date)
            data_content['Expiry'].append(expiry)
            data_content['Renewed'].append(renewed)
            
            browser.back()
        
        # Check next consecutive pages
        check_next_page(browser)
        time.sleep(10)
    
    browser.quit()

    # Store the dictionary data to as CSV file
    save_csv_to_extraction(cwd, data_content, ln, lt)
    print(f'\tTotal runtime: {time.time() - t}')
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ln', help='A keyword for Last Name', required=True, type=str)
    parser.add_argument('--lt', choices=range(1, 12), 
                        help=
                        '''
                        License Type
                        DEFAULT: 1 - All
                        2 - Certified Pharmacy Technician
                        3 - Intern - Graduate
                        4 - Intern - Student
                        5 - Non-Resident Pharmacist
                        6 - Non-Resident PIC
                        7 - Pharmacist
                        8 - Pharmacy Technician
                        9 - Pharmacy Technician in Training
                        10 - Practitioner Controlled Substance 
                        11 - Researcher Controlled Substance
                        12 - Student Pharmacy Technician
                        ''',
                        default=1,
                        required=False,
                        type=int,
                        metavar='[1-11]'
                        )
    
    args = parser.parse_args()
    
    main(args)