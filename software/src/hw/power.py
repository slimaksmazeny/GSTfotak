import socket, shutil

def pisugar(cmd, host="127.0.0.1", port=8423, timeout=1.0):
    """pisugar-server (instaluje se skriptem PiSugar) poslouchá na TCP 8423.
    Odpověď je ve tvaru 'battery: 86.4'."""
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall((cmd + "\n").encode())
        resp = s.recv(256).decode().strip()
    return resp.split(":", 1)[1].strip() if ":" in resp else resp

def battery_status():
    # OVĚŘIT přesné názvy příkazů v dokumentaci PiSugar Power Manager
    return {"percent": float(pisugar("get battery")),
            "voltage": float(pisugar("get battery_v")),
            "charging": pisugar("get battery_charging") == "true"}

def cpu_temp():
    return int(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000

def disk_free_gb(path="/home/cam/photos"):
    return round(shutil.disk_usage(path).free / 1e9, 1)
