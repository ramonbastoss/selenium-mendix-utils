from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pyperclip
from datetime import datetime
from pathlib import Path
import os
from faker import Faker
import random
import requests
import re



# Constantes
TIMEOUT = 3



# Funções
def wait(driver):  # wait “global”
    return WebDriverWait(driver, TIMEOUT)

def get_by_css(driver, css):
    element = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return element

def click_css(driver, css):
	el = get_by_css(driver, css)
	el.click()
    return el

def click_xpath(driver, xp):
    el = wait(driver).until(EC.element_to_be_clickable((By.XPATH, xp)))
    el.click()
    return el

def type_css(driver, css, text):
    el = get_by_css(css)
    el.clear()
    el.send_keys(text)
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



# funções mendix
def get_button(driver ,button_name: str):
    css = 'button.mx-name-' + button_name
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def get_by_id(driver, id_value: str):
    css = f"[id*='{id_value}']"
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def get_by_class(driver, class_value):
    css = f"[class*='{class_value}']"
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def set_input(driver, input_name: str, text):
    inp = get_by_id(driver, input_name)
    inp.send_keys(text)


def paste_on_input(driver, input_name: str, text_to_paste):
    input_field = get_by_id(driver, input_name)
    driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
    input_field.click()
    pyperclip.copy(text_to_paste)
    input_field.send_keys(Keys.CONTROL, 'v')


def get_checkbox(driver, checkbox_name):
    el = get_by_id(driver, checkbox_name)
    return el

def get_button(driver ,button_name):
    css = 'button.mx-name-' + button_name
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def get_link_button(driver ,link_button_name):
    css = 'a.mx-name-' + link_button_name
    el = wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    return el

def get_container(driver, container_name):
    container = get_by_class(driver, container_name)
    return container


def set_combobox(driver, combobox_name, option_text):
    css = 'div.mx-name-' + combobox_name
    cbox = get_by_css(driver, css)
    driver.execute_script("arguments[0].scrollIntoView(true);", cbox)
    cbox.click()
    wait(driver).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-content, .select-options, ul[role='listbox']"))
    )
    option = wait(driver).until(
        lambda d: cbox.find_element(By.XPATH, f".//span[normalize-space()='{option_text}']")
    )
    wait(driver).until(lambda d: option.is_displayed() and option.is_enabled())
    option.click()
    return option

def drop_file(driver, file_path):
    filedropper = wait(driver).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id='input-file-upload']")))
    filedropper.send_keys(file_path)
    # driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}))", filedropper)
    

