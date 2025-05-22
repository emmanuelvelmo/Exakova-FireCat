import pyautogui
import time

# Cerrar ventana de resolución
def sys_cerrar_res():
    time.sleep(2)
    pyautogui.moveTo(850, 90)
    pyautogui.click()
    time.sleep(1)

# Cerrar ventana
def sys_cerrar_ventana():
    pyautogui.hotkey('alt', 'f4')
    time.sleep(2)

# Abrir Chromium
def sys_abrir_chr():
    # Abrir Chromium desde el menú de aplicaciones
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.typewrite("chromium")
    pyautogui.press('enter')
    time.sleep(20)
    pyautogui.press('f11')
    time.sleep(1)

# Abrir Waydroid
def sys_abrir_wd():
    # Abrir Chromium desde el menú de aplicaciones
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.typewrite("waydroid")
    pyautogui.press('enter')
    time.sleep(60)
