# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wiki
def execute(args):
    if not args:
        print()
        return

description = "Выводит текст"

    # Склеиваем аргументы
text = " ".join(args)
    
    # Обрабатываем escape-последовательности (как \n, \t)
try:
        text = text.encode('utf-8').decode('unicode_escape')
except:
        pass
        
print(text)