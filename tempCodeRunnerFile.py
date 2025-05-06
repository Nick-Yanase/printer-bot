 WebDriverWait(navegador, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "deviceconfig"))
        )