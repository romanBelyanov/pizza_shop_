import json
import view

from odbc import progError


def age_check(age):
    if age >= 18:
        return True
    return False

def new_session(name, password, age):
    with open("now_session.json", 'w') as file:
        user_data = {
            "name": name,
            "password": password,
            "age": age,
            "shoppings": []
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
                new_session(name, password, age)
            try:
                with open("data_user.json", 'w') as file:
                    json.dump(user_data, file, ensure_ascii=False, indent=4)
            except:
                pass
        else:
            print("Это имя занято")

    def login():
        try:
            with open("data_user.json", 'r') as file:
                g = 0
                user_data = json.load(file)
                if user_data["users"] == []:
                    print("Сначала зарегистрируйтесь")
                    signin_or_login(view.hi())
                login = input()
                password = input()

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







