import base64
from collections.abc import Set
from pathlib import Path

imagen_b64 = base64.b64encode(
    Path(r"C:\Users\jimma\Downloads\papas.jpg").read_bytes()
).decode("ascii")

print(imagen_b64)

#$bytes = [System.IO.File]::ReadAllBytes("C:\Users\jimma\Downloads\papas.jpg")
# Set-Clipboard -Value ([Convert]::ToBase64String($bytes))