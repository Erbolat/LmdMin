from flask import Flask, render_template_string
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
    options = Options()
    options.headless = True
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=options)
    url = "https://lmd.up.railway.app/"
    element_id = "lmdValue"
    result = get_data_by_id_with_selenium(driver, url, element_id)
    driver.quit()

    # HTML-шаблон с встроенным результатом
    html_content = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Результат</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 50px;
                background-color: #f4f4f4;
            }}
            h1 {{
                color: #333;
            }}
            p {{
                font-size: 1.2em;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <h1>Извлеченные данные:</h1>
        <p>{result}</p>
    </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True)
