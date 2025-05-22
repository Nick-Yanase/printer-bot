from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista de IPs das impressoras
ips = [
    "172.16.18.2", #funcionando recepca-pso
    "172.16.17.5", # erro de segurança da pagina | recepcao psa
    "172.16.24.14"
    
]

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Rodar sem abrir a janela
chrome_options.add_argument('--disable-gpu')  # Melhor performance no Windows
chrome_options.add_argument('--no-sandbox')  # Necessário em alguns ambientes
chrome_options.add_argument('--window-size=1920,1080')  # Tamanho fixo para evitar bugs
chrome_options.add_argument("--ignore-certificate-errors")  # Ignora erro de HTTPS
chrome_options.add_argument("--allow-insecure-localhost")   # Permite localhost inseguro
chrome_options.add_argument("--allow-running-insecure-content")


# Pega o driver compatível com a versão do navegador do usuário
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

for ip in ips:
    try:
        print(f"\nAcessando impressora no IP: {ip}")
    
        # -------- 1. Obtendo o CONTADOR --------
        navegador.get(f"https://{ip}/web/guest/en/websys/status/getUnificationCounter.cgi")
        navegador.implicitly_wait(5)

        elemento_cont = navegador.find_elements(By.CLASS_NAME, "staticProp")

        if len(elemento_cont) >= 2:
            segundo_elemento = elemento_cont[1]
            tds = segundo_elemento.find_elements(By.TAG_NAME, "td")
            contador = tds[3].text if len(tds) > 3 else "Contador não encontrado"
        else:
            contador = "Elemento staticProp insuficiente"

        print(f"Contador: {contador}")

        # -------- 2. Obtendo o ID da Impressora 

        navegador.get(f"https://{ip}/web/guest/en/websys/status/configuration.cgi")

        navegador.implicitly_wait(3)

        # Acha o menu que contém os dados de id equipamento
        menu_id = navegador.find_element(By.XPATH, "//tr[contains(@class, 'staticProp')][td[contains(text(), 'Machine ID')]]")
        
        #pega o 4º td que contém o id do equipamento
        num_serie = menu_id.find_element(By.XPATH, "./td[4]").text
      
          # -------- Resultado final --------
        print(f"IP: {ip}")
        print(f"Contador: {contador}")
        print(f"ID Impressora: {num_serie}")

    except Exception as e:
        print(f"Erro ao acessar IP {ip}: {e}")

# Fecha o navegador no final
navegador.quit()
