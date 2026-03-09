# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wiki
import os

description = "Очищает экран"

def execute(args):
    os.system('/bin/clear')