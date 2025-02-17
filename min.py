import logging
import schedule
import time
import os
import subprocess
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
        
        # Ждем, пока текст элемента не изменится (если начальное значение "0.00")
        WebDriverWait(driver, 20).until(
            lambda driver: element.text.strip() != "0.00"
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

def write_to_file(result):
    # Получаем текущее время и вычитаем 1 час для получения предыдущего
    current_time = datetime.now() - timedelta(hours=1)
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M")
    
    # Запись данных в файл
    with open(r"C:\Users\ADMIN\Desktop\result.txt", "a") as file:
        file.write(f"{formatted_time}, {result}\n")
        logging.info(f"Данные записаны в файл: {formatted_time}, {result}")

def job(driver):
    url = "https://lmd.up.railway.app/"
    element_id = "lmdValue"
    
    # Получаем данные с сайта
    result = get_data_by_id_with_selenium(driver, url, element_id)
    
    # Записываем данные в файл
    logging.info(f"Извлеченные данные: {result}")

if __name__ == "__main__":
    # Настроим параметры браузера для работы в фоне (headless режим)
    options = Options()
    options.headless = True  # Включаем headless режим
    options.add_argument("--no-sandbox")  # Отключает песочницу
    options.add_argument("--disable-dev-shm-usage")  # Отключает использование общей памяти
    options.add_argument("--disable-gpu")  # Отключает использование GPU
    options.add_argument("--disable-software-rasterizer")  # Отключает использование программного рендеринга
    options.add_argument("--disable-background-networking")  # Отключает фоновую сетевую активность
    options.add_argument("--disable-default-apps")  # Отключает использование стандартных приложений

    # Инициализация ChromeDriver с использованием настроенных параметров
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=options)

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
