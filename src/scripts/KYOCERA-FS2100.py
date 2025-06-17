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
  "172.16.18.101",
  "172.16.17.3", 
  "172.16.3.4",
  
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
        navegador.get(f"http://{ip}")
        navegador.maximize_window()

        # ✅ Verifica se a página inicial está acessível (ex: frame de login)
        try:
            WebDriverWait(navegador, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "wlmframe"))
            )
        except:
            raise Exception("Frame de login não disponível ou IP inacessível.")

        # Continua a lógica normalmente (sem mais verificações individuais)
        input_user = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "arg01_UserName"))
        )
        input_user.send_keys("Admin")

        input_pass = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "arg02_Password"))
        )
        input_pass.send_keys("Admin")

        btn_login = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @class='mauth']"))
        )
        btn_login.click()

        item_config = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[font[contains (text(), 'Configurações')]]"))
        )
        item_config.click()

        navegador.switch_to.default_content()

        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "main"))
        )

        printer_itens = navegador.find_elements(By.XPATH, "//font[@face='Verdana']")
        num_serie = printer_itens[1].text

        menu_counter = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "parentcounters"))
        )
        menu_counter.click()

        navegador.switch_to.default_content()

        WebDriverWait(navegador, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "main"))
        )
        counter_itens = navegador.find_elements(By.XPATH, "//font[@face='Verdana']")
        contador = counter_itens[0].text

        # ✅ Adiciona o resultado se deu tudo certo
        resultados.append({
            "ip": ip,
            "modelo": "KYOCERA FS2100",
            "contador": contador,
            "numero_serie": num_serie,
            "obs": "✅"
        })

    except Exception as e:
        resultados.append({
            "ip": ip,
            "modelo": "KYOCERA FS2100",
            "contador": "❌",
            "numero_serie": "❌",
            "obs": str(e)
        })


navegador.quit()

print(json.dumps(resultados, indent=4, ensure_ascii=False))