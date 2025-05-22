from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista de IPs das impressoras
ips = [
    "172.16.17.27",
    "172.16.17.23",
    "172.16.9.26",
    #"172.16.9.203"
]

chrome_options = Options()
chrome_options.add_argument('--headless')   # Rodar sem abrir a janela
chrome_options.add_argument('--disable-gpu')  # Melhor performance no Windows
chrome_options.add_argument('--no-sandbox')  # Necessário em alguns ambientes
chrome_options.add_argument('--window-size=1920,1080')  # Tamanho fixo para evitar bugs

# Pega o driver compatível com a versão do navegador do usuário
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

for ip in ips:
    try:
        print(f"\nAcessando impressora no IP: {ip}")
        
        navegador.get(f"http://{ip}")
        navegador.maximize_window()
        
        # Espera um pouquinho
        navegador.implicitly_wait(5)
        
        # -------- 1. Obtendo o CONTADOR --------

        # Acha o <td> pelo texto 'Counter' e clica
        pag_contador = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Counter']")
        navegador.execute_script("arguments[0].click();", pag_contador)

        time.sleep(0.5)

        contador = navegador.find_element(By.XPATH, "//td[@class='settingCategoryL2' and @nowrap]/following-sibling::td[@nowrap][1]").text
        # contador = menu_contador.find_element(By.XPATH, "./tr[2]/td[3]").text
      

        # -------- 2. Obtendo o ID da Impressora 
        # Acha o <td> pelo texto 'Machine Information' e clica
        pag_information = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Machine Information']")
        pag_information.click()

        time.sleep(0.5)

        tds = navegador.find_elements(By.XPATH, "//td[@class='settingCategoryL2' and @nowrap]")
        num_serie = tds[2].find_element(By.XPATH, "./following-sibling::td[@nowrap]").text

        # # -------- Resultado final --------
        print(f"Contador: {contador}")
        print(f"ID Impressora: {num_serie}")
    except Exception as e:
        print(f"Erro ao acessar IP {ip}: {e}")

navegador.quit()


