#!/usr/bin/python3.15
import os, sys, importlib.util
# Сделано https://github.com/attackuwu под лицензией GPL-2.0
# Документация: https://github.com/attackuwu/pynux/wiki
try: import readline
except: pass

COMMANDS_DIR = "/system/shell/commands"
shell_env = {"__builtins__": __builtins__}

def load_cmd(name):
    path = os.path.join(COMMANDS_DIR, f"{name}.py")
    if not os.path.exists(path): return None

    if name in sys.modules:
        del sys.modules[name]
    
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)

        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f"Ошибка загрузки {name}: {e}")
        return None

def pynux_shell():
    print("\033[2J\033[H\033[1;36mPynux Alpha\033[0m")
    while True:
        try:
            inp = input(f"\x01\033[1;32m\x02pynux\x01\033[0m\x02:\x01\033[1;34m\x02{os.getcwd()}\x01\033[0m\x02# ").strip()
            if not inp: continue
            
            parts = inp.split()
            cmd_name = parts[0]
            args = parts[1:]
            
            # Сначала проверяем, есть ли такой файл (он тперь всегда грузится заново)
            mod = load_cmd(cmd_name)
            if mod:
                if hasattr(mod, 'execute'):
                    mod.execute(args)
                continue
                
            # Если файла нет — Даем пробовать Python
            try:
                res = eval(inp, shell_env)
                if res is not None: print(repr(res))
            except (SyntaxError, NameError):
                try:
                    exec(inp, shell_env)
                except Exception:
                    print(f"pynux: команда не найдена: {cmd_name}")
            except Exception as e:
                print(f"Python error: {e}")
                
        except KeyboardInterrupt: print()
        except EOFError: break

if __name__ == "__main__":
    if not os.path.exists(COMMANDS_DIR): os.makedirs(COMMANDS_DIR)
    pynux_shell()