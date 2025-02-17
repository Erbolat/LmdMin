from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_data_by_id_with_selenium(driver, url, element_id):
    driver.get(url)
    logging.info("Инициализация браувывывывзера...")
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        data = element.text.strip()
        return data if data else "Данные не найдены"
    except Exception as e:
        return f"Ошибка: {e}"

@app.route('/')
def index():
    logging.info("Инициализация браузера...")
    options = Options()
    options.headless = True
    # service = Service(ChromeDriverManager().install())
    service = Service()  # Создаем сервис для Chrome
    driver = webdriver.Chrome(service=service, options=options) 
    url = "https://lmd.up.railway.app/"
    element_id = "lmdValue"
    result = get_data_by_id_with_selenium(driver, url, element_id)
    driver.quit()
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
