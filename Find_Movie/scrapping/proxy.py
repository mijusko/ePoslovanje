from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
import config


def get_random_proxy():
    """Get a random proxy from the list."""
    return random.choice(config.ips)


def create_chrome_with_proxy(proxy):
    """Create a Chrome WebDriver instance with the specified proxy."""
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')

    # Update this path to your chromedriver
    service = Service('C:/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def main():
    proxy = get_random_proxy()
    driver = create_chrome_with_proxy(proxy)

    print(proxy)
    # Example usage
    driver.get('https://www.example.com')
    # print(f'Using proxy: {proxy}')

    # Add your code to interact with the website

    driver.quit()


if __name__ == "__main__":
    main()
