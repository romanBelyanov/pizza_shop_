import json
import view

def summ():
    shops_sum = 0
    with open("now_session.json", 'r') as session:
        data = json.load(session)
        shoppings = data["shoppings"]
        prices = data["prices"]
    for amount in prices:
        shops_sum += int(amount)
    return shops_sum, shoppings, prices
def age_check(age):
    if 18 <= age <= 60:
        return True
    return False

def new_session(name, password, age):
    with open("now_session.json", 'w') as file:
        user_data = {
            "name": name,
            "password": password,
            "age": age,
            "shoppings": [],
            "prices": []
        }
        json.dump(user_data, file)
    view.show_menu()

def is_available(name):
    with open("data_user.json", 'r') as file:
        user_data = json.load(file)
        for i in range(len(user_data["users"])):
            if name == user_data["users"][i]["login"]:
                print(f"У вас уже есть учетная запись")
                return False
    return True


def signin_or_login(num):
    def signin():
        name = input("Введите логин: ")
        password = input("Введите пароль: ")
        age = int(input("Введите возраст: "))
        if is_available(name):
            data = {
                "login": name,
                "password": password,
                "age": age
            }
            with open("data_user.json", 'r') as file:
                user_data = json.load(file)
                user_data = user_data["users"]
                user_data.append(data)
                user_data = {
                    "users": user_data
                }
                print("Успешная регистрация")
            with open("data_user.json", 'w') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
            new_session(name, password, age)

    def login():
        try:
            with open("data_user.json", 'r') as file:
                g = 0
                user_data = json.load(file)
                if user_data["users"] == []:
                    print("Сначала зарегистрируйтесь")
                    signin_or_login(view.hi())
                login = input("Введите логин: ")
                password = input("Введите пароль: ")

                for i in range(len(user_data["users"])):
                    if login == user_data["users"][i]["login"] and password == user_data["users"][i]["password"]:
                        print(f"Вы вошли как {login}")
                        g = 1
                        new_session(user_data["users"][i]["login"], user_data["users"][i]["password"],
                                    user_data["users"][i]["age"])

                if g == 0:
                    print("Авторизация не удалась. Попробуйте ещё раз")
                    signin_or_login(2)
        except:
            pass

    if num == 1:
        signin()
    elif num == 2:
        login()

def display_receipt(order, total, payment_method, cash_given=None):
    """Выводит чек."""

    print("\n==============================")
    print("            Ваш чек:         ")
    print("------------------------------")
    for item in order:
        print(f"{item[0]}: {item[1]} руб.")
        del_product(item[0])
    print("------------------------------")
    print(f"Итого: {total} руб.")
    print(f"Способ оплаты: {payment_method}")
    if cash_given:
        change = cash_given - total
        print(f"Сдача: {change} руб.")
    print("==============================")

def do_order():
    order = input("Введите номер продукта или его название (если хотите закончить, введите 0 или конец): ")
    order = order.lower()
    while order != "0" and order.lower() != "конец":
        with open("now_session.json", "r") as f:
            session = json.load(f)
            age = session['age']
            name = session['name']
            password = session['password']
        with open("menu.json", "r") as fi:
            menu = json.load(fi)
            menu = menu['menu']
        shops = session['shoppings']
        prices = session['prices']
        pizzas = ["margherita", "pepperoni", "hawaiian", "vegetarian"]
        drinks = ["coca-cola", "sprite", "mineral water"]
        alcohol = ["beer", "wine", "mojito"]
        try:
            order = int(order)
            if 1 <= order <= 4:
                for i in menu['pizzas']:
                    if i['key'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
            if 5 <= order <= 7:
                for i in menu['drinks']:
                    if i['key'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
            if 8 <= order <= 10 and age_check(age):
                for i in menu['alcohol']:
                    if i['key'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
        except:
            if order in pizzas:
                for i in menu['pizzas']:
                    if i['name'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
            if order in drinks:
                for i in menu['drinks']:
                    if i['name'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
            if order in alcohol and age_check(age):
                for i in menu['alcohol']:
                    if i['name'] == order:
                        shops.append(i['name'])
                        prices.append(i['price'])
        with open("now_session.json", "w") as file:
            data = {
                    "name": name,
                    "password": password,
                    "age": age,
                    "shoppings": shops,
                    "prices": prices
            }
            json.dump(data, file)
        order = input("Введите номер продукта или его название (если хотите закончить, введите 0 или конец): ")
    summa = summ()
    display_receipt(zip(summa[1], summa[2]), summa[0], "наличные")


def del_product(product):
    with open("menu.json", "r") as f:
        menu = json.load(f)
    with open("now_session.json", "r") as f:
        session = json.load(f)
    for food in menu["menu"]:
        if food == 'alcohol' and not age_check(session["age"]):
            continue
        for data in menu["menu"][food]:
            if data["name"] == product:
                if data["kol"] > 0:
                    data["kol"] -= 1
    with open("menu.json", "w") as f:
        json.dump(menu, f, indent=4)