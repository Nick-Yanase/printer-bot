from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

ips = [
    "172.16.18.202", 
    ]


chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--allow-running-insecure-content")

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

for ip in ips:
    try:
        # -------- 1. Obtendo o CONTADOR --------
        print(f"\nAcessando impressora no IP: {ip}")
        navegador.get(f"http://{ip}")
        navegador.maximize_window()
        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
        )
        menu_principal = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[font[contains(text(), 'Dados do dispositivo')]]"))
        )

        menu_principal.click()

        contador_item = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[font[contains(text(), 'Contador')]]"))
        )
        contador_item.click()
        
        # Aguarda o iframe 'printingjobs' aparecer e troca para ele
        WebDriverWait(navegador, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "deviceconfig"))
        )
        # tr que possui um td com o texto total
        tr_contador = navegador.find_element(By.XPATH, "//tr[td[contains(text(), 'Total')]]")

        contador = tr_contador.find_element(By.XPATH, "./td[3]").text


        # -------- 2. Obtendo o ID da Impressora 
        navegador.get(f"http://{ip}")
        navegador.maximize_window()
        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
        )
        menu_principal = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[font[contains(text(), 'Dados do dispositivo')]]"))
        )

        menu_principal.click()

        contador_item = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[font[contains(text(), 'Configuração')]]"))
        )
        contador_item.click()
        
        WebDriverWait(navegador, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "printingjobs"))
        )
        # Aguarda o span com id 'w272px' ficar visível
        serial_span = navegador.find_elements(By.ID, "w272px")
        # Obtém o texto do serial number
        id_printer = serial_span[3].text

        # # -------- Resultado final --------
        print(f"Contador: {contador}")
        print(f"ID Impressora: {id_printer}")

        
    except Exception as e:
        print(f"Erro ao acessar IP {ip}: {e}")

navegador.quit()