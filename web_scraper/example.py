from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd


target_url = "https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniqBStoreParam1=val1&wid=11.productCard.PMU_V2"


def example_webdriver():
    driver = webdriver.Chrome("/home/yichen/side_projects/web_scraper/chromedriver")
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    print(driver.title)
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    driver.close()


if __name__ == "__main__":
    # driver = webdriver.Chrome('/home/yichen/side_projects/web_scraper/chromedriver')
    # driver.get(target_url)
    products = []  # List to store name of the product
    prices = []  # List to store price of the product
    ratings = []  # List to store rating of the product
    # content = driver.page_source
    # print(content)
    content = requests.get(target_url).content
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.findAll("a", "_1fQZEK"):
        name = a.find("div", "_4rR01T")
        price = a.find("div", "_30jeq3 _1_WHN1")
        rating = a.find("div", "_3LWZlK")
        products.append(name.text)
        prices.append(price.text)
        ratings.append(rating.text)

    dataframe = pd.DataFrame(
        {"Product Name": products, "Price": prices, "Rating": ratings}
    )
    dataframe.to_csv("example.csv", encoding="utf-8")
