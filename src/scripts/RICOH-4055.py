from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ips = [
    "172.16.17.101",
]
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

for ip in ips:
  try:

    wait = WebDriverWait(navegador, 3)
    # ------- obtendo ID ----------
    navegador.get(f"http://{ip}/web/guest/br/websys/status/configuration.cgi")

    menu_serie = wait.until(EC.presence_of_element_located((
            By.XPATH, "//tr[contains(@class, 'staticProp')][td[contains(text(), 'ID da máquina')]]"
        )))
    num_serie = menu_serie.find_element(By.XPATH, "./td[4]").text

    # ------- obtendo CONTADOR ---------
    navegador.get(f"http://{ip}/web/guest/br/websys/status/getUnificationCounter.cgi")

    menu_contador = wait.until(EC.presence_of_element_located((
            By.XPATH, "//tr[contains(@class, 'staticProp')][td[contains(text(), 'Total')]]"
        )))
    contador = menu_contador.find_element(By.XPATH, "./td[4]").text
    # ------ resultados armazenados ------
    resultados.append({
            "ip": ip,
            "modelo": "RICOH 4055",
            "contador": contador,
            "numero_serie": num_serie,
            "obs": "✅"
        })
    
  except Exception as e:
    resultados.append({
            "ip": ip,
            "modelo": "RICOH 4055",
            "contador": "❌",
            "numero_serie": "❌",
            "obs": str(e)
        })

# Fecha o navegador
navegador.quit()

# Exibe os resultados
print(json.dumps(resultados, indent=4, ensure_ascii=False))