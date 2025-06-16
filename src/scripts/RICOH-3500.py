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

# Lista de IPs das impressoras
ips = [
    "172.16.9.40", 
    "172.16.9.70", 
    "172.16.9.110",
    "172.16.9.204",
    "172.16.17.30", 
    "172.16.17.36", 
    "172.16.17.105", 
]

# Configuração do navegador (apenas uma vez)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

resultados = []

for ip in ips:
    try:
        navegador.get(f"http://{ip}")

        wait = WebDriverWait(navegador, 3)

        # Abrindo aba de contador
        pag_contador = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='tabUnSelected']/a[text()='Counter']")))
        navegador.execute_script("arguments[0].click();", pag_contador)

        contador = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "p5_0_0_0"))).text

        # Abrindo aba de informações
        pag_information = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Machine Information']")
        navegador.execute_script("arguments[0].click();", pag_information)

        elementos_info = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "p5_0_0_0")))
        num_serie = elementos_info[2].text if len(elementos_info) >= 3 else '❌'

        resultados.append({
            "ip": ip,
            "modelo": "RICOH 3510",
            "contador": contador,
            "numero_serie": num_serie,
            "obs": "✅"
        })

    except Exception as e:
        resultados.append({
            "ip": ip,
            "modelo": "RICOH 3510",
            "contador": '❌',
            "numero_serie": '❌',
            "obs": str(e)
        })

# Fecha o navegador no final
navegador.quit()

print(json.dumps(resultados, indent=4))
