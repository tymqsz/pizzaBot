from typing import List
from pizza import Pizza
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

class PizzaBot:
    def __init__(self, data, driver):
        self.data = data
        self.driver = driver

        self.pizza_cnt = None
        self.payment_method = None

    def wait_and_click(self, wait_time: int, element: str, method=By.XPATH, possible_skip=False) -> bool:
        if not possible_skip:
            button = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((method, element))
            )
            button.click()
        else:
            try:
                button = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((method, element))
                )
                button.click()
            except:
                return False
        return True

    def wait_and_send_keys(self, wait_time: int, element: str, to_send: str, method=By.XPATH, possible_skip=False) -> bool:
        if not possible_skip:
            input_bar = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((method, element))
            )
            input_bar.send_keys(to_send)
            input_bar.send_keys(Keys.RETURN)
        else:
            try:
                input_bar = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((method, element))
                )
                input_bar.send_keys(to_send)
                input_bar.send_keys(Keys.RETURN)
            except:
                return False
        return True

    def prepare(self):
        self.driver.get('https://pizzahut.pl/en')
        self.driver.maximize_window()

        self.wait_and_click(10, 'onetrust-accept-btn-handler', By.ID)

        adress_bar = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="search-input"]'))
        )
        adress_bar.send_keys(self.data.ADRESS)
        time.sleep(2)
        adress_bar.send_keys(Keys.RETURN)

        self.wait_and_click(10, '//*[@id="location-picker"]/div/button')
        self.wait_and_click(2, '//*[@id="modal-root"]/div[2]/div[2]/div/div[2]/div[2]/button[1]', possible_skip=True)
        self.wait_and_click(1, '//*[@id="modal-root"]/div/div[2]/div/div/div[2]/button[2]', possible_skip=True)
        self.wait_and_click(3, "//button//p[text()='Order takeaway']", possible_skip=True)
        self.wait_and_click(1, '//*[@id="__next"]/div/div/div[1]/div/ul/li[5]', possible_skip=True)

    def order(self, pizzas: List[Pizza], payment_method: str):
        self.pizza_cnt = len(pizzas)
        self.payment_method = payment_method

        for i in range(self.pizza_cnt):
            crt_pizza = pizzas[i]

            span_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//span[text()='PIZZA']")))
            pizza_category = span_element.find_element(By.XPATH, "./ancestor::a")
            self.driver.execute_script("arguments[0].click();", pizza_category)

            for s in range(16):
                xpath = f'//*[@id="category-2765--tiles--tiles"]/li[{str(s + 1)}]'

                if s == 3 or s == 7 or s == 11 or s == 15:
                    self.driver.execute_script("window.scrollTo(0, window.scrollY + 240)")
                text = str(self.driver.find_element(By.XPATH, xpath).text)

                split = text.split()
                name = split[0] + ' ' + split[1]
                if name.upper() == crt_pizza.getName():
                    xpath = f'//*[@id="category-2765--tiles--tiles"]/li[{str(s + 1)}]'
                    self.wait_and_click(2, xpath)
                    break

            self.wait_and_click(3, '//*[@id="modal-root"]/div/div[2]/div/section/span', possible_skip=True)

            if crt_pizza.getDough() == "pan":
                self.wait_and_click(5, '//*[@id="__next"]/div/div/div[1]/main/section[1]/div/div[3]/ul/li[2]/span')

            if crt_pizza.getSize() == "large":
                self.wait_and_click(5, '//*[@id="__next"]/div/div/div[1]/main/section[1]/div/div[4]/ul/li[2]/span')

            self.wait_and_click(10, '//*[@id="__next"]/div/div/div[1]/main/section[1]/div/div[1]/div/button')
            self.wait_and_click(1, '//*[@id="modal-root"]/div/div[2]/div/div[2]/div[2]/button[1]', possible_skip=True)

            time.sleep(1)

        order_clicked = self.wait_and_click(2, "//button[text()='Order']", possible_skip=True)
        if not order_clicked:
            raise Exception("your order is too small")

        self.wait_and_click(2, '//*[@id="modal-root"]/div/div[2]/div/div[2]/div[2]/button[1]', possible_skip=True)
        self.wait_and_click(2, '//*[@id="modal-root"]/div/div[2]/div/div/div[2]/button[2]', possible_skip=True)

        self.wait_and_send_keys(3, '//*[@id="checkout--customer--first-name"]', to_send=self.data.NAME)
        self.wait_and_send_keys(3, '//*[@id="checkout--customer--email"]', to_send=self.data.EMAIL)
        self.wait_and_send_keys(3, '//*[@id="checkout--customer--phone"]', to_send=self.data.PHONE_NR)
        self.wait_and_send_keys(3, '//*[@id="checkout--delivery-address--flat-number"]',
                                to_send=self.data.FLAT_NR, possible_skip=True)

        if payment_method == 'blik':
            self.wait_and_click(2, '//*[@id="__next"]/div/div/div[1]/form/main/div/section[4]/div/div/div[1]/ul/li[1]/div/div')
        else:
            self.wait_and_click(2, '//*[@id="__next"]/div/div/div[1]/form/main/div/section[4]/div/div/div[2]/ul/li['
                              '2]/div/div/div[2]')

        self.wait_and_click(2, '//*[@id="__next"]/div/div/div[1]/form/main/div/div[1]/div[1]/div/label[1]')

    def finalize(self):
        assert(self.payment_method is not None)
        assert(self.pizza_cnt is not None)

        summary = ''
        for i in range(self.pizza_cnt):
            xpath = f'//*[@id="basket"]/div/div[3]/ul/li[{i + 1}]/div'

            crt_pizza = self.driver.find_element_by_xpath(xpath).text

            if i != 0:
                summary += f", {crt_pizza}"
            else:
                summary += f"{crt_pizza}"

        total_cost = self.driver.find_element_by_xpath('//*[@id="basket"]/div/div[4]/div[2]/span[2]').text

        print('Your order:', end="\n")
        print(summary, end="\n\n")
        print('total cost: ', total_cost, end="\n\n")

        confirm = input('to confirm write \"CONFIRM\" :')
        if confirm == "CONFIRM":
            self.countdown(10, 'ordering in sec', 12)

            self.wait_and_click(2, '//*[@id="price-button"]')

            if self.payment_method == 'blik':
                self.driver.maximize_window()
        else:
            print('transaction cancelled')
            self.driver.quit()

    @staticmethod
    def countdown(peroid, output, place):
        for i in range(peroid, -1, -1):
            final_output = '\r' + output[:place] + ' ' + str(i) + ' ' + output[place:]
            sys.stdout.write(final_output)
            time.sleep(1)