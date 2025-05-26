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
    "172.16.17.16"
    ]

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--allow-running-insecure-content")

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

resultados = []

for ip in ips:
    try:
        # -------- 1. Obtendo o CONTADOR --------
        navegador.get(f"http://{ip}")
        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
        )
        menu_principal = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'P001_menu_main') and (contains(@class, 'closed') or contains(@class, 'opened'))][.//span[contains(text(), 'Dados do dispositivo')]]"))
        )
        menu_principal.click()

        submenu = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".P001_menu_sub"))
        )
        contador_item = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "s81"))
        )
        contador_item.click()
        # Aguarda o iframe 'printingjobs' aparecer e troca para ele
        WebDriverWait(navegador, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "deviceconfig"))
        )
        # tr que possui um td com o texto total
        tr_contador = navegador.find_element(By.XPATH, "//tr[td[contains(text(), 'Total')]]")
        contador = tr_contador.find_element(By.XPATH, "./td[3]").text


        # -------- 2. Obtendo o ID da Impressora 
        navegador.get(f"http://{ip}")
        # Troca para o frame onde está o menu (nome correto: 'wlmframe')
        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
        )
        menu_principal = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'P001_menu_main') and (contains(@class, 'closed') or contains(@class, 'opened'))][.//span[contains(text(), 'Dados do dispositivo')]]"))
        )
        menu_principal.click()

        # Aguarda o submenu aparecer, senão aparecer lança um exception
        submenu = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".P001_menu_sub"))
        )
        # Aguarda o item "Configuração" ficar clicável pelo ID
        configuracao_item = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "s80"))
        )
        configuracao_item.click()
        # Aguarda o iframe 'printingjobs' aparecer e troca para ele
        WebDriverWait(navegador, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "printingjobs"))
        )
        serial_span = navegador.find_elements(By.ID, "w272px")
        num_serie = serial_span[3].text

        # -------- Resultado final --------
        resultados.append({
           "ip": ip,
           "modelo": "KYOCERA M3145",
           "contador": contador,
           "numero_serie": num_serie,
           "obs": "✅"
           }
        )

        
    except Exception as e:
        resultados.append({
            "ip": ip,
            "modelo": "KYOCERA M3145",
            "contador": "❌",
            "numero_serie": "❌",
            "obs": str(e)
        })

navegador.quit()
print(json.dumps(resultados, indent=4, ensure_ascii=False))