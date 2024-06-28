class Pizza:
    name_dict = {
        'margherita': 'MARGHERITA PIZZA',
        'pepperoni': 'PEPPERONI PIZZA',
        'hawajska': 'HAWAIIAN PIZZA',
        'americana': 'AMERICANA PIZZA',
        'texas': 'TEXAS PIZZA',
        'miesna': 'MEAT PIZZA',
        'vege': 'VEGE MANIA PIZZA',
        'classica': 'CLASSICA PIZZA',
        'europejska': 'EUROPEAN PIZZA',
        'hot pepperoni': 'HOT PEPPERONI PIZZA',
        'farmerska': 'FARMER PIZZA',
        'capriccosa': 'CAPRICCOSA PIZZA',
        'carbonara': 'CARBONARA PIZZA',
        'prosciutto': 'PROSCIUTTO PIZZA',
        'supreme': 'SUPREME PIZZA',
        'super supreme': 'SUPER SUPREME PIZZA'
    }

    def __init__(self, name, size, dough_type):
        if name not in Pizza.name_dict.keys():
            raise Exception("IncorrectPizzaNameException")
        else:
            self._name = Pizza.name_dict[name]

        self._size = size
        self._dough_type = dough_type

    def getName(self):
        return self._name

    def getSize(self):
        return self._size

    def getDough(self):
        return self._dough_type