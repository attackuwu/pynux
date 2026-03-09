# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wiki
import os

description = "Менеджер пакетов Python"

def execute(args):
    if not args:
        print("Использование: pip <команда> [опции]")
        return
    
    # Пробрасываем все аргументы в оригинальный модуль pip
    args_str = " ".join(args)
    # Используем встроенный pip Python 3.15
    os.system(f"/usr/bin/python3.15 -m pip {args_str}")