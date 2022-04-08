# -*- coding: utf-8 -*-
import time
import datetime
import random
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException



class P2pBuyNgnSpider(scrapy.Spider):
    name = 'p2p_buy_ngn'

    MIN_TIME = 3
    MAX_TIME = 10

    def __init__(self, fiat=None, crypto=None, side=None):
        self.side = side
        self.crypto = crypto
        self.fiat = fiat

    def start_requests(self):

        valid_params = all(
            [self.side,
            self.crypto,
            self.fiat]
        )

        if valid_params:

            yield SeleniumRequest(
                url=f"https://p2p.binance.com/en/trade/{self.side}/{self.crypto}?fiat={self.fiat}&payment=ALL",
                wait_time=13,
                screenshot=True,
                callback=self.parse,
                meta={
                    'side' : self.side,
                    'crypto' : self.crypto,
                    'fiat' : self.fiat,
                }
            )

    def parse(self, response):
        # img = response.meta['screenshot']
        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)

        driver = response.meta['driver']
        side = response.meta['side']
        crypto = response.meta['crypto']

        try:
            cancel_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-ebuj64 svg')))
            cancel_button.click()
            print("=========Cancel Button Found=====")
        except (TimeoutException, WebDriverException) as e:
            print("=========No Cancel Button Found=====")

        # next_page_button = driver.find_element_by_xpath(
        #     "//button[@class='mirror css-1w7smpm']//*[local-name() = 'svg']")
        # if next_page_button:
        #     next_page_button.click()
        #     # time.sleep(3)

        # driver.save_screenshot("screenshot1.png")
        page = 1
        while True:
            html = driver.page_source
            response_obj = Selector(text=html)

            time_stamp = datetime.datetime.now()

            buyers = response_obj.xpath("//div[@class='css-tsk0hl']")

            for buyer in buyers:
                
                name = buyer.xpath(".//div[@class='css-1rhb69f']/a/text()").get()
                link = buyer.xpath(".//div[@class='css-1rhb69f']/a/@href").get()
                completed = buyer.xpath(".//div[@class='css-19crpgd']/text()").get()
                order_count = buyer.xpath(".//div[@class='css-1a0u4z7']/text()").get()
                price = buyer.xpath(".//div[@class='css-1m1f8hn']/text()").get()
                currency = buyer.xpath(".//div[@class='css-dyl994']/text()").get()

                available = buyer.xpath("(.//div[@class='css-3v2ep2']/div)[2]/text()").get()
                low_limit = buyer.xpath("(.//div[@class='css-4cffwv'])[1]/text()").get()
                high_limit = buyer.xpath("(.//div[@class='css-4cffwv'])[2]/text()").get()
                payment = buyer.xpath("(.//div[@class='css-1n3cl9k']/div)[1]/div/text()").get()


                
                yield {
                    "name" : name,
                    "link" : link,
                    "completed" : completed,
                    "order_count": order_count,
                    "price" : price,
                    "currency": currency,
                    "available" : available,
                    "low_limit" : low_limit,
                    "high_limit": high_limit,
                    "payment" : payment,
                    'crypto' : crypto,
                    'side' : side,
                    'date': time_stamp,
                }
            # break
            # next_page_button = driver.find_element_by_xpath(
            #     "//button[@aria-label='Next page']")
            # if next_page_button:
            #     driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(
            #         driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))))
            #     print("============", next_page_button, "================")
            #     driver.save_screenshot("shot.png")
            #     time.sleep(3)
            #     break
            # else:
            #     break
            # break
            page += 1
            try:
                driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(
                    driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']"))))
                driver.find_element_by_xpath(
                    "//button[@aria-label='Next page']").click()
                print(f"==================Navigating to Next Page : page {page}=======================")
                time.sleep(random.randint(self.MIN_TIME, self.MAX_TIME))
            except (TimeoutException, WebDriverException) as e:
                print("=====================Last page reached===========================")
                break

        driver.quit()

