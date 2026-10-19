import json
import os
import struct
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus

PASTA = Path(__file__).resolve().parent

# Códigos de tecla do Linux (input-event-codes.h)
KEY_LEFTCTRL, KEY_W, KEY_PAGEUP = 29, 17, 104

_uinput_fd = None


def _uinput():
    """Cria (uma vez) um teclado virtual em /dev/uinput; funciona em X11 e Wayland."""
    global _uinput_fd
    if _uinput_fd is None:
        import fcntl

        fd = os.open("/dev/uinput", os.O_WRONLY | os.O_NONBLOCK)
        fcntl.ioctl(fd, 0x40045564, 1)  # UI_SET_EVBIT, EV_KEY
        for tecla in (KEY_LEFTCTRL, KEY_W, KEY_PAGEUP):
            fcntl.ioctl(fd, 0x40045565, tecla)  # UI_SET_KEYBIT
        # struct uinput_setup: input_id (bustype, vendor, product, version), nome, ff_effects_max
        fcntl.ioctl(fd, 0x405C5503, struct.pack("HHHH80sI", 0x03, 0x1234, 0x5678, 1, b"pesquisar-teclado", 0))
        fcntl.ioctl(fd, 0x5501)  # UI_DEV_CREATE
        time.sleep(1)  # dá tempo do sistema reconhecer o dispositivo
        _uinput_fd = fd
    return _uinput_fd


def _evento(fd, tipo, codigo, valor):
    os.write(fd, struct.pack("llHHi", 0, 0, tipo, codigo, valor))


def _atalho_linux(modificador, tecla):
    fd = _uinput()
    for codigo, valor in ((modificador, 1), (tecla, 1), (tecla, 0), (modificador, 0)):
        _evento(fd, 1, codigo, valor)
        _evento(fd, 0, 0, 0)  # SYN_REPORT
        time.sleep(0.05)


def _atalho_windows(modificador, tecla):
    import ctypes

    keybd_event = ctypes.windll.user32.keybd_event
    for vk, flags in ((modificador, 0), (tecla, 0), (tecla, 2), (modificador, 2)):
        keybd_event(vk, 0, flags, 0)  # flags 2 = KEYUP
        time.sleep(0.05)


def fechar_aba_anterior():
    """Volta para a aba anterior (Ctrl+PageUp) e a fecha (Ctrl+W); o foco fica na aba nova."""
    if sys.platform == "win32":
        VK_CONTROL, VK_PRIOR, VK_W = 0x11, 0x21, 0x57
        _atalho_windows(VK_CONTROL, VK_PRIOR)
        time.sleep(0.3)
        _atalho_windows(VK_CONTROL, VK_W)
    else:
        try:
            _atalho_linux(KEY_LEFTCTRL, KEY_PAGEUP)
            time.sleep(0.3)
            _atalho_linux(KEY_LEFTCTRL, KEY_W)
        except OSError as erro:
            print(f"Não foi possível enviar teclas ({erro}). Sem permissão em /dev/uinput?")


with open(PASTA / "pesquisas.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

for i, item in enumerate(dados):
    frase = item["pesquisa"]
    url = "https://www.google.com/search?q=" + quote_plus(frase)

    print(f"Pesquisando: {frase}")

    webbrowser.open(url, new=2)

    time.sleep(1)

    if i > 0:
        fechar_aba_anterior()

    time.sleep(4)

print("Todas as pesquisas foram realizadas")
