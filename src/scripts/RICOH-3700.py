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

# Lista de IPs das impressoras
ips = [
    "172.16.17.27", 
    #"172.16.17.23", administrativo
    "172.16.24.3",
    "172.16.9.26", 
    #"172.16.9.20", # PRT-TRIAGEM PSI- BLOCO A bugada
]

# Configuração do navegador (única vez)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

resultados = []
try:
    for ip in ips:
        try:
            navegador.get(f"http://{ip}")
            wait = WebDriverWait(navegador, 3)

            # -------- 1. Obtendo o CONTADOR --------
            pag_contador = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='tabUnSelected']/a[text()='Counter']")))
            navegador.execute_script("arguments[0].click();", pag_contador)

            contador = wait.until(EC.presence_of_element_located((
                By.XPATH, "//td[@class='settingCategoryL2' and @nowrap]/following-sibling::td[@nowrap][1]"
            ))).text

            # -------- 2. Obtendo o NÚMERO DE SÉRIE --------
            pag_information = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//td[@class='tabUnSelected']/a[text()='Machine Information']"
            )))
            navegador.execute_script("arguments[0].click();", pag_information)

            tds = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//td[@class='settingCategoryL2' and @nowrap]"
            )))

            num_serie = tds[2].find_element(By.XPATH, "./following-sibling::td[@nowrap]").text if len(tds) >= 3 else '❌'

            # -------- Resultado final --------
            resultados.append({
                "ip": ip,
                "modelo": "RICOH 3710",
                "contador": contador,
                "numero_serie": num_serie,
                "obs": "✅"
            })

        except Exception as e:
            resultados.append({
                "ip": ip,
                "modelo": "RICOH 3710",
                "contador": '❌',
                "numero_serie": '❌',
                "obs": str(e)
            })

finally:
    # Fecha o navegador no final
    kill_chrome_driver_tree(navegador)
    # Saída formatada
    print(json.dumps(resultados, indent=4))
