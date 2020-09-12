from pypresence import Presence
from datetime import datetime
import requests
import time
import sys

monitoring_url = "https://cristalix.ru/data/technical/mcinfo" # Адрес для получения онлайна автоматически
client_id = "733090650945224724"  # ID Discord приложения

# Получение онлайна на выбраном сервере
def getOnline(servername):
    response = requests.get(monitoring_url)
    req = response.json()
    for server in req["info"]:
        if servername == server["name"]:
            playerCount = " (" + str(server["players"]) + \
                " из " + str(server["maxPlayers"]) + ")"
    return playerCount

print("cristalixRPC by ethernalsteve\n")

try:
    # Ввод никнейма
    username = input("Введите ник: ")

    # Выбор сервера
    try:
        server = int(input("Выберете сервер (1 - NeoTech, 2 - Magica, 3 - SkyTechVoid, 4 - TechnoMagic, 5 - DivinePVP): "))
        if server == 1:
            serverImage = "neotech"
            serverName = "NeoTech"
        elif server == 2:
            serverImage = "magica"
            serverName = "Magica"
        elif server == 3:
            serverImage = "skytechvoid"
            serverName = "SkyTechVoid"
        elif server == 4:
            serverImage = "technomagic"
            serverName = "TechnoMagic"
        elif server == 5:
            serverImage = "divinepvp"
            serverName = "DivinePVP"
        else:
            print("Ошибка при указании номера сервера.")
            sys.exit()
    except ValueError:
        print("Ошибка при указании номера сервера.")
        sys.exit()

    # Выбор статуса
    try:
        status = int(input("Ваш статус (1 - В меню, 2 - В игре): "))
        if status == 1:
            status = "В меню"
        elif status == 2:
            playerCount = input("Онлайн на сервере. Оставьте пустым для автоматического определения (в формате \"1 из 100\"): ")
            if playerCount == "":  # Автоматическое определение онлайна
                status = serverName + getOnline(serverName)
            else:                  # Добавление указанного онлайна
                status = serverName + " (" + playerCount + ")"
        else:
            print("Указан неверный статус.")
            sys.exit()
    except ValueError:
        print("Указан неверный статус.")
        sys.exit()

    # Количество времени в игре
    try:
        usertime = input("Время в меню/в игре. Оставьте пустым, для отсчёта с 00:00 (в секундах): ")
        if usertime == "":
            usertime = 0
        else:
            usertime = int(usertime)
    except ValueError:
        print("Указано неверное время")
        sys.exit()

    # Подключение к клиенту Discord
    RPC = Presence(client_id)
    RPC.connect()

    # Получаем текущее время
    now = datetime.now()
    starttime = datetime.timestamp(now) - usertime

    # Обновляем статус
    RPC.update(
        details=username,
        state=status,
        start=starttime,
        large_image=serverImage,
        large_text=serverName,
        small_image="small",
        small_text="Cristalix"
    )
    print("\nСтатус успешно изменён! Для закрытия программы используйте Ctrl+C")

    # В бесконечном цикле обновляем статус каждые 5 секунд
    while True:
        if status != "В меню":
            if playerCount == "":  # Автоматическое определение онлайна
                status = serverName + getOnline(serverName)
            else:                  # Добавление указанного онлайна
                status = serverName + " (" + playerCount + ")"
            RPC.update(
                details=username,
                state=status,
                start=starttime,
                large_image=serverImage,
                large_text=serverName,
                small_image="small",
                small_text="Cristalix"
            )
        time.sleep(5)
except KeyboardInterrupt:
    RPC.close()
    print("\nПрограмма была закрыта при помощи Ctrl+C")
except SystemExit:
    print("Выход из программы...")