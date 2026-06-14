import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:5000")

    text_input = driver.find_element(By.ID, "text-input")
    text_input.send_keys("Spotlessly clean rooms with attentive staff and superb amenities throughout")

    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()

    # Give the model ample time to download weights and respond on the first run
    time.sleep(30)

    result_output = driver.find_element(By.ID, "result-output")
    text = result_output.text

    assert text != ""
    driver.quit()
