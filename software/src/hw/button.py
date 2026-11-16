"""Tlačítko je fyzicky na PiSugar 3 (pad 10 <-> BAT). Krátký stisk = foto,
dlouhý stisk řeší PiSugar sám (vypnutí).
Varianta A (reFrame): přímé čtení I2C 0x57 – převzít funkci is_power_button_pressed() z reframe.py.
Varianta B: pisugar-server posílá připojeným TCP klientům události tlačítka.  # OVĚŘIT na HW
"""
import socket

def button_events(host="127.0.0.1", port=8423):
    with socket.create_connection((host, port)) as s:
        for line in s.makefile():
            ev = line.strip()
            if ev in ("single", "double", "long"):
                yield ev
