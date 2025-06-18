import psutil
 #Finaliza o processo do ChromeDriver e todos os seus filhos (incluindo o Chrome).
def kill_chrome_driver_tree(driver):
    try:
        driver_process = psutil.Process(driver.service.process.pid)
        for child in driver_process.children(recursive=True):
            child.kill()
        driver_process.kill()
    except Exception as e:
        print("Erro ao finalizar o ChromeDriver:", str(e))