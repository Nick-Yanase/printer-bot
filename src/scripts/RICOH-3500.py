from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Lista de IPs das impressoras
ips = [
    "172.16.9.100",
    "172.16.9.40",
    "172.16.9.70",
    "172.16.9.110",
    "172.16.9.204",
    "172.16.17.30",
    "172.16.17.36",
    "172.16.17.105",
    "172.16.24.190",
]

# Configurações do Chrome para rodar em modo invisível
chrome_options = Options()
chrome_options.add_argument('--headless')  # Rodar sem abrir a janela
chrome_options.add_argument('--disable-gpu')  # Melhor performance no Windows
chrome_options.add_argument('--no-sandbox')  # Necessário em alguns ambientes
chrome_options.add_argument('--window-size=1920,1080')  # Tamanho fixo para evitar bugs

# Pega o driver compatível com a versão do navegador do usuário
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

resultados = []

for ip in ips:
    try:
        navegador.get(f"http://{ip}")
        navegador.maximize_window()
    
        navegador.implicitly_wait(5)

        pag_contador = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Counter']")
        navegador.execute_script("arguments[0].click();", pag_contador)
        time.sleep(0.5)
        contador = navegador.find_element(By.CLASS_NAME, "p5_0_0_0").text

        pag_information = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Machine Information']")
        pag_information.click()
        time.sleep(0.5)
        elementos_info = navegador.find_elements(By.CLASS_NAME, "p5_0_0_0")
        num_serie = elementos_info[2].text

        resultados.append({
            "ip": ip,
            "contador": contador,
            "numero_serie": num_serie,
            "obs": ""
        })
    
    except Exception as e:
        resultados.append({
            "ip": ip,
            "contador":'x',
            "numero_serie": 'x',
            "obs": str(e)
        })

# Fecha o navegador no final
navegador.quit()
print(json.dumps(resultados))