import subprocess

def run_cmd(cmd_list):
    print(f"[*] Выполняю: {' '.join(cmd_list)}")
    try:
        subprocess.run(cmd_list)
    except Exception as e:
        print(f"[-] Критическая ошибка: {e}")

def init():
    print("\n[pynit] Инициализация сети...")
    # 2. ПОДНИМАЕМ ИНТЕРФЕЙСЫ
    run_cmd(["/bin/busybox", "ifconfig", "lo", "up"])
    run_cmd(["/bin/busybox", "ifconfig", "eth0", "up"])
    run_cmd(["/bin/busybox", "ifconfig", "eth0", "10.0.2.15", "netmask", "255.255.255.0"])
    run_cmd(["/bin/busybox", "route", "add", "default", "gw", "10.0.2.2"])
    
    print("[+] Сетевые интерфейсы сконфигурированы.\n")

if __name__ == "__main__":
    init()