import os
import importlib.util

description = "Выводит этот текст"

def execute(args):
    # Путь к директории с командами
    commands_dir = "/system/shell/commands"
    
    # Если путь не существует (например, при тестах на другой машине), 
    # берем путь относительно текущего файла
    if not os.path.exists(commands_dir):
        commands_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\nСписок доступных команд Pynux:")
    print("-" * 50)
    
    try:
        # Получаем список всех .py файлов, кроме начинающихся на __
        files = [f for f in sorted(os.listdir(commands_dir)) 
                 if f.endswith(".py") and not f.startswith("__")]
        
        for filename in files:
            command_name = filename[:-3]  # Убираем .py
            file_path = os.path.join(commands_dir, filename)
            
            # Динамически загружаем модуль для чтения переменной description
            description = "Описание отсутствует"
            try:
                spec = importlib.util.spec_from_file_location(command_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Проверяем, есть ли в файле переменная description
                if hasattr(module, 'description'):
                    description = module.description
            except Exception:
                # Если файл не удалось импортировать, просто идем дальше
                pass
            
            # Вывод: имя команды выравниваем по левому краю (15 символов)
            print(f"  {command_name:<15} | {description}")
            
    except Exception as e:
        print(f"Ошибка при сканировании команд: {e}")
        
    print("-" * 50 + "\n")