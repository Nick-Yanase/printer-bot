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

ips = [
    "172.16.18.100",
]

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--allow-running-insecure-content")

# Instancia o navegador
navegador = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)

resultados = []

try:
    for ip in ips:
        try:
            wait = WebDriverWait(navegador, 3)
            # -------- Obtendo o CONTADOR --------
            navegador.get(f"http://{ip}/web/guest/en/websys/status/getUnificationCounter.cgi")

            elementos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "staticProp")))

            if len(elementos) >= 2:
                segundo = elementos[1]
                tds = segundo.find_elements(By.TAG_NAME, "td")
                contador = tds[3].text if len(tds) > 3 else "❌ Contador não encontrado"
            else:
                contador = "❌ Dados insuficientes para contador"

            # -------- Obtendo o ID da Impressora --------
            navegador.get(f"http://{ip}/web/guest/en/websys/status/configuration.cgi")

            menu_id = wait.until(EC.presence_of_element_located((
                By.XPATH, "//tr[contains(@class, 'staticProp')][td[contains(text(), 'Machine ID')]]"
            )))

            num_serie = menu_id.find_element(By.XPATH, "./td[4]").text

            resultados.append({
                "ip": ip,
                "modelo": "RICOH 4500",  # ou o modelo que você quiser descrever
                "contador": contador,
                "numero_serie": num_serie,
                "obs": "✅"
            })

        except Exception as e:
            resultados.append({
                "ip": ip,
                "modelo": "RICOH 4500",
                "contador": "❌",
                "numero_serie": "❌",
                "obs": str(e)
            })

finally:
    # Fecha o navegador
    kill_chrome_driver_tree(navegador)
    # Exibe os resultados
    print(json.dumps(resultados, indent=4))
