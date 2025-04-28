from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista de IPs das impressoras
ips = [
    "172.16.9.204",
    "172.16.9.100",
    "172.16.9.40",
    "172.16.9.70",
    "172.16.9.110",
    "172.16.9.204",
    "172.16.17.30",
    "172.16.24.19",
]

# Configurações do Chrome para rodar em modo invisível
chrome_options = Options()
chrome_options.add_argument('--headless')  # Rodar sem abrir a janela
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

        # Acha o <td> pelo texto 'Counter' e clica
        pag_contador = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Counter']")
        navegador.execute_script("arguments[0].click();", pag_contador)

        time.sleep(0.5)

        # Devolve o número do contador
        contador = navegador.find_element(By.CLASS_NAME, "p5_0_0_0").text
        print(f"Contador: {contador}")

        # Acha o <td> pelo texto 'Machine Information' e clica
        pag_information = navegador.find_element(By.XPATH, "//td[@class='tabUnSelected']/a[text()='Machine Information']")
        pag_information.click()

        time.sleep(0.5)

        # Pega os elementos da página de info e devolve o número de série
        elementos_info = navegador.find_elements(By.CLASS_NAME, "p5_0_0_0")
        num_serie = elementos_info[2].text
        print(f"Número de Série: {num_serie}")
    
    except Exception as e:
        print(f"Erro ao acessar IP {ip}: {e}")

# Fecha o navegador no final
navegador.quit()
