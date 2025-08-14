from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# import time
# from pathlib import Path
# import os
# from faker import Faker
# import random

import pyperclip
from datetime import datetime
import requests
import re

# Funções
def get_by_id(driver, id_value: str):
    css = f"[id*='{id_value}']"
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def click_xpath(driver, xp):
    el = wait(driver).until(EC.element_to_be_clickable((By.XPATH, xp)))
    el.click()
    return el
    
def now():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return timestamp

def today():
    timestamp = datetime.now().strftime("%d/%m/%Y")
    return timestamp

def gerar_cep_mock():
    url = "https://www.4devs.com.br/ferramentas_online.php"
    payload = {
        "acao": "gerar_cep",
        "pontuacao": "S"  # "S" = com hífen, "N" = sem hífen
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.post(url, data=payload, headers=headers)
    resp.raise_for_status()
    match = re.search(r'<div id="cep".*?><span>(\d{5}-\d{3})</span>', resp.text)
    if match:
        return match.group(1)
    else:
        raise ValueError("CEP não encontrado no retorno.")


class MendixDriver:
    def __init__(self, driver, timeout = 3):
        self.driver = driver
        self.timeout = timeout

    # métodos mais genêricos
    def wait(self):
        return WebDriverWait(self.driver, self.timeout)
        
    # def get_page_name(self):
    #     driver = self.driver
    #     self.wait_page_load()
    #     self.wait().until(
    #         lambda d: d.execute_script("return mx.ui.getContentForm().path").strip() != ''
    #     )
    #     path = driver.execute_script("return mx.ui.getContentForm().path;")
    #     start = path.rfind('/') + 1
    #     end = path.find('.')
    #     page_name = path[start:end]
    #     return page_name
        
    def get_by_css(self, css):
        element = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return element
    
    def get_by_class(self, class_value):
        css = f"[class*='{class_value}']"
        el = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return el

    def click_css(driver, css):
        el = get_by_css(css)
        el.click()
        return el

    def get_by_xpath(self, xp):
        el = self.wait().until(EC.element_to_be_clickable((By.XPATH, xp)))
        return el
    
    # métodos mais específicos
    def get_input(self, input_name):
        css = f"input[id*='{input_name}']"
        el = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return el
        
    def get_button(self, button_name):
        css = 'button.mx-name-' + button_name
        el = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return el

    def click_button(self, button_name):
        self.get_button(button_name).click()

    def set_input(self, id_value: str, text):
        inp = self.get_input(id_value)
        inp.clear()
        inp.send_keys(text)


    def paste_on_input(self, input_name: str, text_to_paste):
        driver = self.driver
        input_field = get_by_id(driver, input_name)
        driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        input_field.click()
        pyperclip.copy(text_to_paste)
        input_field.send_keys(Keys.CONTROL, 'v')


    def get_checkbox(self, checkbox_name):
        el = get_by_id(self.driver, checkbox_name)
        return el

    def get_button(self ,button_name):
        css = 'button.mx-name-' + button_name
        el = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return el

    def get_link_button(self ,link_button_name):
        css = 'a.mx-name-' + link_button_name
        el = self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        return el

    def get_container(self, container_name):
        container = self.get_by_class(container_name)
        return container
        
    def click_container(self, container_name):
        container = self.get_by_class(container_name)
        container.click()
        return container

    def set_combobox(self, combobox_name, option_text):
        driver = self.driver
        css = 'div.mx-name-' + combobox_name
        cbox = get_by_css(css)
        driver.execute_script("arguments[0].scrollIntoView(true);", cbox)
        cbox.click()
        self.wait().until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-content, .select-options, ul[role='listbox']"))
        )
        option =self.wait().until(
            lambda d: cbox.find_element(By.XPATH, f".//span[normalize-space()='{option_text}']")
        )
        self.wait().until(lambda d: option.is_displayed() and option.is_enabled())
        option.click()
        return option

    def drop_file(self, file_path):
        driver = self.driver
        filedropper = self.wait().until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id='input-file-upload']")))
        filedropper.send_keys(file_path)
        # driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}))", filedropper)
    

