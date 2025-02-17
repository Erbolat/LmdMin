import logging
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_by_id_with_selenium(driver, url, element_id):
    # Переход на страницу с использованием уже открытого браузера
    driver.get(url)

    try:
        logging.info(f"Ожидаем появления элемента с ID: {element_id}")
        
        # Ждем, пока элемент с данным ID не появится на странице (до 20 секунд)
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        
        # Извлекаем текстовое содержимое элемента
        data = element.text.strip()

        if not data:
            logging.warning(f"Элемент с ID '{element_id}' найден, но текст пуст.")
            return "Элемент найден, но текст пуст."
        
        logging.info(f"Извлеченные данные: {data}")
        return data
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return f"Ошибка: {e}"



def job(driver):
    url = "https://lmd.up.railway.app/"
    element_id = "lmdValue"
    
    # Получаем данные с сайта
    result = get_data_by_id_with_selenium(driver, url, element_id)
    
    # Записываем данные в файл
    logging.info(f"Извлеченные данные: {result}")  # Исправлен отступ

if __name__ == "__main__":
    # Настраиваем параметры браузера
    options = Options()
    options.headless = True  # Включаем headless режим
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    # Инициализация ChromeDriver с использованием настроенных параметров
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # Планируем выполнение задачи каждые 2 минуты
    schedule.every(2).minutes.do(job, driver)

    # Запускаем бесконечный цикл для выполнения задач
    logging.info("Запуск планировщика задач...")
    try:
        while True:
            schedule.run_pending()  # Проверка на выполнение запланированных задач
            time.sleep(1)  # Пауза в 1 секунду между проверками
    finally:
        # Закрываем браузер при завершении работы скрипта
        driver.quit()
        logging.info("Браузер закрыт.")
