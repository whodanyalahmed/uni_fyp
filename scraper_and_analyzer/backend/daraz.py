from lib2to3.pgen2.driver import Driver
from selenium import webdriver
import os
import re
from scraper_and_analyzer.models import Dataset

chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

def Chrome(headless=False):
    # add fake user agent
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=chrome_options)
    driver.implicitly_wait(5)
    return driver
def minpr(d):
    if d == 0:
        return 100000000000000000000
    else:
        return 1


def daraz_main(keyword, choice):
    minprice = minpr(0)
    minname = ""
    mincount = 0

    keyword_url = keyword.replace(' ', '+')

    url = 'https://www.daraz.pk/smartphones/?from=input&q=' + keyword_url
    
    driver = Chrome(True)
    driver.get(url)
    # find div with id root
    root = driver.find_element_by_id('root')
    # find div with class product-list

    product_div = root.find_element_by_xpath(
        '//div[@data-qa-locator="general-products"]')
    products_card = product_div.find_elements_by_xpath(
        '//div[@class="gridItem--Yd0sa"]')



    product = product_div.find_elements_by_xpath(
        '//div[@class="inner--SODwy"]')

    title = product_div.find_elements_by_xpath(
        '//div[@class="title--wFj93"]')
    price = product_div.find_elements_by_xpath(
        '//div[@class="price--NVB62"]')
    # img_Src = product_div.find_elements_by_xpath(
    #     '//img[@class="image--WOyuZ "]')
    # get img with class image--WOyuZ and also have alt attribute
    img_Src = product_div.find_elements_by_xpath(
        '//img[@class="image--WOyuZ " and @alt]')

    price_list = []
    title_list = []
    image_list = []
    link_list = []
    for i in range(len(title)):
        link = product[i].find_element_by_xpath(
            'div[1]/div/a').get_attribute('href')

        int_price = price[i].text.replace('Rs. ', '')
        int_price = int_price.replace(',', '')
        int_price = int(int_price)

        obj, created = Dataset.objects.get_or_create(
            name=title[i].text, price=int_price, website='daraz', image=img_Src[i].get_attribute('src'), link=link)

        fname = title[i].text.lower()
        keyword_name = keyword.lower().split(' ')
        # get keyword_name except first one
        # keyword_name = keyword_name[1:]
        if keyword.lower() in fname:

            link_list.append(link)
            # check if same price is found then skip
            title_list.append(title[i].text)

            price_list.append(int_price)
            image_list.append(img_Src[i].get_attribute('src'))

    # print(product.text)
    dt = dict(zip(title_list, price_list))

    for k, v in dt.items():

        if v < minprice:
            minprice = v
            minname = k

    print("Min. price is : ", minprice)

    # return minprice,minname and iamge_link with mincount as index

    driver.quit()
    index = price_list.index(minprice)
    if choice == "result":

        return {"price": minprice, "name": minname, "src": image_list[index], "link": link_list[index]}
    else:
        return {"names": title_list, "prices": price_list, "images": image_list, "links": link_list}


if __name__ == '__main__':
    d = daraz_main("Iphone 13")
    print(d)
