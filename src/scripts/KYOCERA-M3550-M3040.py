from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys
import os

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.chrome_utils import kill_chrome_driver_tree

sys.stdout.reconfigure(encoding='utf-8')
ips = ["172.16.18.202", "172.16.24.19"]

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--allow-running-insecure-content")

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

resultados = []
try:
    for ip in ips:
        try:
            navegador.get(f"http://{ip}")

            WebDriverWait(navegador, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
            )

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[font[contains(text(), 'Dados do dispositivo')]]"))
            ).click()

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[font[contains(text(), 'Contador')]]"))
            ).click()

            WebDriverWait(navegador, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "deviceconfig"))
            )

            contador = navegador.find_element(
                By.XPATH, "//tr[td[contains(text(), 'Total')]]/td[3]"
            ).text

            navegador.get(f"http://{ip}")

            WebDriverWait(navegador, 15).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
            )

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[font[contains(text(), 'Dados do dispositivo')]]"))
            ).click()

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[font[contains(text(), 'Configuração')]]"))
            ).click()

            WebDriverWait(navegador, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "printingjobs"))
            )

            num_serie = navegador.find_elements(By.ID, "w272px")[3].text

            # ------ resultados armazenados ------
            resultados.append({
                "ip": ip,
                "modelo": "KYOCERA M3550",
                "contador": contador,
                "numero_serie": num_serie,
                "obs": "✅"
            })

        except Exception as e:
            resultados.append({
                "ip": ip,
                "modelo": "KYOCERA M3550",
                "contador": "❌",
                "numero_serie": "❌",
                "obs": str(e)
            })

finally:
    kill_chrome_driver_tree(navegador)
    print(json.dumps(resultados, indent=4, ensure_ascii=False))