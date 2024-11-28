import json
import model
def hi():
    print("Здравствуйте! Выберите действие:")
    print("1 - Регистрация")
    print("2 - Авторизация")
    ans = int(input())
    if ans >= 2:
        return 2
    else:
        return 1

def show_menu():
    dct = {"pizzas": "Пиццы:", "drinks": "Напитки: ", "alcohol": "Алкоголь: "}
    with open("now_session.json", "r") as file:
        text = json.load(file)
    with open("menu.json", "r") as file:
        res = json.load(file)
    for food in res['menu']:
        if food == 'alcohol' and not model.age_check(text["age"]):
            continue
        print(dct[food])
        for param in res['menu'][food]:
            print(f"Название: {param['name']} Цена: {param['price']}")