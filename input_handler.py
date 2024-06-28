from pizza import Pizza


class InputHandler:
    standard_order = [
        Pizza("texas", "medium", "light"),
        Pizza("pepperoni", "large", "pan")
    ]

    def __init__(self):
        self._order = []
        self._payment_method = None

    def takeOrder(self):
        print("Welcome to pizza hut. Type your answers and confirm by pressing ENTER")

        if input("do you wanna get your standard order? (Y/N)").strip().lower() == "y":
            self._order = InputHandler.standard_order
        else:
            while True:
                cnt_input = input("how many pizzas? ")
                if cnt_input.isdigit():
                    pizza_cnt = cnt_input
                    break
                else:
                    print("recived incorrect count")

            for i in range(pizza_cnt):
                while True:
                    pizza_name = input(f"pizza {i+1}. name: ").lower().strip()
                    if pizza_name not in Pizza.name_dict.keys():
                        print("recived incorrect name")
                    else:
                        break
                while True:
                    pizza_size = input(f"pizza {i + 1}. size: ").lower().strip()
                    if pizza_size != "medium" and pizza_size != "large":
                        print("recived incorrect size, possible sizes: medium/large")
                    else:
                        break
                while True:
                    pizza_dough = input(f"pizza {i + 1}. dough: ").lower().strip()
                    if pizza_dough != "pan" and pizza_dough != "light":
                        print("recived incorrect dough, possible doughs: pan/light")
                    else:
                        break

                self._order.append(Pizza(pizza_name, pizza_size, pizza_dough))

        while True:
            payment = input("do you wanna pay with blik or on arrival? ")
            if payment != "blik" and payment != "on arrival":
                print("recived incorrect payment method, possible: blik/on arrival")
            else:
                break

        self._payment_method = payment

    def getOrder(self):
        return self._order

    def getPayment(self):
        return self._payment_method