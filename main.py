from input_handler import InputHandler
from metadata import Data
from pizza_bot import PizzaBot

from selenium import webdriver

data_path = "mydata.txt"

data = Data(data_path)

driver = webdriver.Chrome()

driver.minimize_window()

inputHandler = InputHandler()
inputHandler.takeOrder()

pizzaBot = PizzaBot(data, driver)
pizzaBot.prepare()
pizzaBot.order(inputHandler.getOrder(), inputHandler.getPayment())

if data.FINALIZATION_PERMIT == "YES":
    pizzaBot.finalize()

