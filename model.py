import json
import random
import segno
import view

def summ(promocode=None):
    shops_sum = 0
    percent = 0
    if promocode != None:
        print(1)
        with open("promocodes.json", "r") as file:
            code = json.load(file)['promocodes']
            for i in code:
                if promocode == i['promocode']:
                    percent = i['percent']
    with open("now_session.json", 'r') as session:
        data = json.load(session)
        shoppings = data["shoppings"]
        prices = data["prices"]
    for amount in prices:
        shops_sum += int(amount)
    shops_sum = shops_sum / 100 * (100 - percent)
    return shops_sum, shoppings, prices, percent
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
    if name == "admin":
        admin()
    else:
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
            with open("log.txt", "r", encoding="utf-8") as file:
                text = str(file.read())
            log = f"\nПользователь {data['login']} зарегистрировался"
            text += log
            with open("log.txt", "w", encoding="utf-8") as file:
                file.write(text)
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
                        with open("log.txt", "r", encoding="utf-8") as file:
                            text = str(file.read())
                        log = f"\nПользователь {login} успешно прошел авторизацию"
                        text += log
                        with open("log.txt", "w", encoding="utf-8") as file:
                            file.write(text)
                        new_session(user_data["users"][i]["login"], user_data["users"][i]["password"],
                                    user_data["users"][i]["age"])

                if g == 0:
                    print("Авторизация не удалась. Попробуйте ещё раз")
                    with open("log.txt", "r", encoding="utf-8") as file:
                        text = str(file.read())
                    log = f"\nПользователь {login} не смог успешно пройти авторизацию"
                    text += log
                    with open("log.txt", "w", encoding="utf-8") as file:
                        file.write(text)
                    signin_or_login(2)
        except:
            pass

    if num == 1:
        signin()
    elif num == 2:
        login()


def display_receipt(order, total, percent, payment_method, cash_given=None):
    """Выводит чек."""
    dct = {}
    prices = {}
    for item in order:
        if item[0] in list(dct.keys()):
            dct[item[0]] = dct[item[0]] + 1
        else:
            dct[item[0]] = 1
        prices[item[0]] = item[1]
    print("==============================")
    print("            Ваш чек:         ")
    print("------------------------------")
    for item in range(len(dct)):
        keys = list(dct.keys())
        values = list(dct.values())
        prices_lst = list(prices.values())
        print(f"{keys[item]} x {values[item]}: {values[item] * prices_lst[item]} руб.")
        for i in range(values[item]):
            del_product(keys[item])
    print(f"Скидка: {percent}%")
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
            if 1 <= int(order) <= 4:
                for i in menu['pizzas']:
                    if i['key'] == order:
                        order = i['name']
                        shops.append(i['name'])
                        prices.append(i['price'])
                        add = input("Хотите ли вы добавку к пицце(если нет, введите 0):")
                        if add == 0:
                            pass
                        else:
                            try:
                                add = int(add)
                                for j in i['adds']:
                                    if j['key'] == add:
                                        shops.append(j['name'])
                                        prices.append(j['price'])
                            except:
                                for j in i['adds']:
                                    if j['name'].lower() == add:
                                        add = j['name']
                                        shops.append(j['name'])
                                        prices.append(j['price'])
            if 5 <= int(order) <= 7:
                for i in menu['drinks']:
                    if i['key'] == order:
                        order = i['name']
                        shops.append(i['name'])
                        prices.append(i['price'])
            if 8 <= int(order) <= 10 and age_check(age):
                for i in menu['alcohol']:
                    if i['key'] == order:
                        order = i['name']
                        shops.append(i['name'])
                        prices.append(i['price'])
        except:
            if order in pizzas:
                for i in menu['pizzas']:
                    if i['name'].lower() == order:
                        order = i['name']
                        shops.append(i['name'])
                        prices.append(i['price'])

            if order in drinks:
                for i in menu['drinks']:
                    if i['name'].lower() == order:
                        order = i['name']
                        shops.append(i['name'])
                        prices.append(i['price'])
            if order in alcohol and age_check(age):
                for i in menu['alcohol']:
                    if i['name'].lower() == order:
                        order = i['name']
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
            with open("log.txt", "r", encoding="utf-8") as file:
                text = str(file.read())
            log = f"\nПользователь {name} заказал {order}"
            text += log
            with open("log.txt", "w", encoding="utf-8") as file:
                file.write(text)
        order = input("Введите номер продукта или его название (если хотите закончить, введите 0 или конец): ")
    promo = input("Промокод (если его нет, введите 0): ")
    if promo == "0":
        summa = summ()
    else:
        summa = summ(promo)
    display_receipt(zip(summa[1], summa[2]), summa[0], summa[3], "наличные")


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
                num = data["kol"]
    for i in menu['menu']['pizzas']:
        for add in i['adds']:
            if add['name'] == product:
                if add['kol'] > 0:
                    add['kol'] -= 1
                num = add['kol']
    with open("menu.json", "w") as f:
        json.dump(menu, f, indent=4)
        with open("log.txt", "r", encoding="utf-8") as file:
            text = str(file.read())
        log = f"\nПродукта {product} осталось {num} штук"
        text += log
        with open("log.txt", "w", encoding="utf-8") as file:
            file.write(text)

def count_product(product):
    with open("menu.json", "r") as f:
        menu = json.load(f)
    for food in menu["menu"]:
        for data in menu["menu"][food]:
            if data["name"] == product:
                print(f"Продукт {product} - {data['col']} штук")

def admin():
    action = input("Вы хотите очистить логи? (да/нет): ")
    if action.lower() == "да":
        with open("log.txt", "w") as w:
            w.write("")
        print("Логи очищены.")
    promo = input("Создать промокод? (да/нет): ")
    if promo.lower() == "да":
        do_promocode()
    history = input("Просмотреть остаток продуктов на складе? (да/нет): ")
    if history.lower() == "да":
        count_product()

def do_promocode():
    lst = list(map(chr, range(65, 90+1)))
    lst.extend(list(map(chr, range(97, 122+1))))
    lst.extend(list(map(chr, range(48, 57+1))))
    percent = random.choice([5, 10, 20, 25, 30])
    promocode = ''.join([random.choice(lst) for i in range(10)])
    qrcode = segno.make_qr(promocode)
    qrcode.save("promocode.png")
    with open("promocodes.json", "r") as file:
        code = json.load(file)['promocodes']
    data = {
        "promocode": promocode,
        "percent": percent
    }
    code.append(data)
    res = {
        "promocodes": code
    }
    with open("promocodes.json", "w") as file:
        json.dump(res, file)
