# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wikiimport subprocess
import sys

description = "Вызывает команду Python"

def execute(args):
    # Если просто ввёл python - запускаем интерактивный режим самого питона
    if not args:
        subprocess.run(["/usr/bin/python3.15"])
        return
    
    # Если python -c "код", выполняем код
    if args[0] == "-c" and len(args) > 1:
        code = args[1]
        try:
            exec(code, globals())
        except Exception as e:
            print(f"Ошибка выполнения: {e}")
    else:
        # Для запуска скриптов, например: python script.py
        subprocess.run(["/usr/bin/python3.15"] + args)