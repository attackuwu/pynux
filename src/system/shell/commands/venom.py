# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wiki
# Внимание! На весь софт Venom распространяется строгая лицензия GPL-2.0
import os
import json
import urllib.request
import ssl
import time

description = "Специальный пакетный менеджер Venom для Pynux"

ssl._create_default_https_context = ssl._create_unverified_context

RAW_URL = "https://raw.githubusercontent.com/attackuwu/venom/main/"
DB_PATH = "/system/var/venom/repo.json"
CMD_DIR = "/system/shell/commands/"

def init_env():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(CMD_DIR, exist_ok=True)

def execute(args):
    init_env()
    
    if not args or not args[0].startswith("-"):
        print("\033[1;35m🐍 Venom Package Manager (v1.1)\033[0m")
        print("  venom -Sy         (Обновить базу пакетов)")
        print("  venom -S <пакет>  (Установить пакет)")
        print("  venom -Ss <имя>   (Найти пакет)")
        print("  venom -R <пакет>  (Удалить пакет)")
        return

    flags = args[0]
    packages = args[1:]

    # 1. ОБНОВЛЕНИЕ БАЗЫ (-Sy)
    if 'y' in flags:
        print("[*] Скачивание repo.json с GitHub...")
        cache_buster = f"?t={int(time.time())}"
        try:
            urllib.request.urlretrieve(RAW_URL + "repo.json" + cache_buster, DB_PATH)
            print("\033[1;32m[+]\033[0m База пакетов синхронизирована!")
        except Exception as e:
            print(f"\033[1;31m[-] Ошибка сети:\033[0m {e}")
        
        if 'S' not in flags or not packages:
            return

    if not os.path.exists(DB_PATH):
        print("[-] Ошибка: База пуста. Сначала выполни 'venom -Sy'.")
        return
        
    try:
        with open(DB_PATH, "r") as f:
            db = json.load(f)
    except:
        print("[-] Ошибка чтения repo.json. Проверь синтаксис на GitHub.")
        return

    # 2. ПОИСК ПАКЕТА (-Ss)
    if 's' in flags:
        query = packages[0] if packages else ""
        for name, info in db.get("packages", {}).items():
            if query in name:
                print(f"\033[1;36mcore/{name}\033[0m - {info.get('description', '')}")
        return

    # 3. УСТАНОВКА ПАКЕТА (-S)
    if 'S' in flags and packages:
        for pkg in packages:
            pkg_data = db.get("packages", {}).get(pkg)
            
            if pkg_data:
                print(f"[*] Установка '{pkg}'...")
                file_path = pkg_data.get("file")
                full_url = f"{RAW_URL}{file_path}?t={int(time.time())}"
                target_path = os.path.join(CMD_DIR, f"{pkg}.py")
                
                try:
                    
                    with urllib.request.urlopen(full_url) as response:
                        if response.status == 200:
                            with open(target_path, "wb") as f:
                                f.write(response.read())
                            print(f"\033[1;32m[+]\033[0m {pkg} успешно установлен в {target_path}")
                        else:
                            print(f"\033[1;31m[-] Ошибка сервера: {response.status}\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[-] Ошибка скачивания {pkg}:\033[0m {e}")
            else:
                print(f"[-] Пакет '{pkg}' не найден в репозитории.")

    # 4. УДАЛЕНИЕ ПАКЕТА (-R)
    if 'R' in flags:
        for pkg in packages:
            try:
                os.remove(f"{CMD_DIR}{pkg}.py")
                print(f"[\033[1;31m-\033[0m] Пакет {pkg} удален.")
            except:
                print(f"[-] Пакет {pkg} не установлен.")