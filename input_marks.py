from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait

# Run this code In the terminal
'"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9111 --no-first-run --no-default-browser-check --user-data-dir="/Users/YourUsername/Library/Application Support/Google/Chrome"'

def main():
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://learn.bcit.ca/d2l/le/activities/iterator/10635681?cft=assignment-submissions&ou=1006061"
               "&currentActorActivityUsage=VG1wWmQwNVdPSGxOUkVGM1dIcFZlVTE2UlhsTmR5NHhNREEyTURZeC5ncm91cF8xMDI5NDkx")
    sleep(5)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next Student"]'))
    )

    # Click the button
    button.click()
    # Use JavaScript to click the custom element
    sleep(3)




    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # driver.close()


if __name__ == '__main__':
    main()