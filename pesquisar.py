import json
import time
import webbrowser
import subprocess
from urllib.parse import quote_plus

with open("pesquisas.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

for item in dados:
    frase = item["pesquisa"]
    url = "https://www.google.com/search?q=" + quote_plus(frase)

    print(f"Pesquisando: {frase}")

    webbrowser.open(url, new=0)

    time.sleep(5)

    subprocess.run([
    "powershell",
    "-Command",
    "$w = New-Object -ComObject WScript.Shell; $w.SendKeys('^w')"
    ])

    time.sleep(1)

print("Todas as pesquisas foram realizadas")