from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_product_info(input_text):
    lines = input_text.strip().split("\n")
    product_info_list = []
    current_product_info = []

    for line in lines:
        if "https://" in line:
            if current_product_info:
                product_info_list.append("\n".join(current_product_info))
                current_product_info = []
            product_info_list.append(line)  # Add image link separately
        else:
            current_product_info.append(line)

    if current_product_info:
        product_info_list.append("\n".join(current_product_info))

    return product_info_list


def fetch_product_details(product_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)


    try:
        driver.get('https://www.flipkart.com')

        # Close the login popup if it appears
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "✕")]'))
            )
            close_button.click()
        except Exception as e:
            pass

        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, '_75nlfW'))
        )

        search_results = driver.find_elements(By.CLASS_NAME, '_75nlfW')

        product_info = []
        for result in search_results:
            img_src = result.find_element(By.TAG_NAME, 'img').get_attribute('src')
            product_info.append(f'{result.text}\n{img_src}\n')

        if product_info:
            text = ''.join(product_info)
            product_info_list = extract_product_info(text)
            info = product_info_list[0].split('\n')[1]
            price = product_info_list[0].split('\n')[2]
            link = product_info_list[1]
            return [info, price, link]
        else:
            return None

    finally:
        driver.quit()


def index3(last_element):
    if last_element:
        query = last_element
    else:
        query = 'none'

    product_details = fetch_product_details(query)
    if product_details:
        product_list = [product_details[0], product_details[2], product_details[1]]
    else:
        product_list = ["spirulina", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK-PXrZIDQbl5zUdfqZmR3VwC3_3WkIgPziw&s", "$345"]

    params = {
        "products": product_list
    }
    return params


def input_form(requests):
    return render(requests, 'search.html')


def submit(requests):
    text_input = requests.POST.get('text_input')
    print(str(text_input)+' vestige assure')
    text_input = str(text_input)+' vestige assure'
    params = index3(text_input)
    print(params)
    return render(requests, 'result.html', params)