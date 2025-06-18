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

ips = [
    "172.16.9.199",
    "172.16.18.3",
    "172.16.5.60",
    "172.16.2.30",
    "172.16.9.100",
    "172.16.12.188",
]

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--allow-running-insecure-content")

navegador = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)

resultados = []

try:
    for ip in ips:
        try:
            wait = WebDriverWait(navegador, 5)
            # ---------- OBTENDO CONTADOR ----------
            navegador.get(f"http://{ip}")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe")))
            menu_principal = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'P001_menu_main') and (contains(@class, 'closed') or contains(@class, 'opened'))][.//span[contains(text(), 'Dados do dispositivo')]]")))
            menu_principal.click()    

            submenu = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".P001_menu_sub"))
            )
            contador_item = wait.until(
                EC.element_to_be_clickable((By.ID, "s81"))
            )
            contador_item.click()
            
            wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "deviceconfig"))
            )
            tr_contador = navegador.find_element(By.XPATH, "//tr[td[contains(text(), 'Total')]]")
            contador = tr_contador.find_element(By.XPATH, "./td[3]").text


            # ---------- OBTENDO NÚMERO DE SÉRIE ----------
            navegador.get(f"http://{ip}")
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
            )
            menu_principal = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'P001_menu_main') and (contains(@class, 'closed') or contains(@class, 'opened'))][.//span[contains(text(), 'Dados do dispositivo')]]"))
            )
            menu_principal.click()
            submenu = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".P001_menu_sub"))
            )
            configuracao_item = wait.until(
                EC.element_to_be_clickable((By.ID, "s80"))
            )
            configuracao_item.click()
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "printingjobs"))
            )
            serial_span = navegador.find_elements(By.ID, "w272px")
            num_serie = serial_span[3].text
            # ---------- RESULTADO ----------
            resultados.append({
                "ip": ip,
                "modelo": "KYOCERA PRINTER",
                "contador": contador,
                "numero_serie": num_serie,
                "obs": "✅"
            })

        except Exception as e:
            resultados.append({
                "ip": ip,
                "modelo": "KYOCERA PRINTER",
                "contador": "❌",
                "numero_serie": "❌",
                "obs": str(e)
            })
finally:
    kill_chrome_driver_tree(navegador)
    print(json.dumps(resultados, indent=4, ensure_ascii=False))
