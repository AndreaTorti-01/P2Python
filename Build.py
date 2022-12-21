import PyInstaller.__main__
import os
import shutil
from pathlib import Path
import platform

PyInstaller.__main__.run([
    'Client.py',
    '--onefile',
    '--noconsole'
])

if (platform.system() == "Windows"):
    shutil.move(Path("dist/Client.exe"), "Client.exe")
else:
    shutil.move(Path("dist/Client"), "Client")
os.remove("Client.spec")

try:
    shutil.rmtree("build")

except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

try:
    shutil.rmtree("dist")

except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

PyInstaller.__main__.run([
    'Server.py',
    '--onefile',
    '--noconsole'
])
if(platform.system() == "Windows"):
    shutil.move(Path("dist/Server.exe"), "Server.exe")
else:
    shutil.move(Path("dist/Server"), "Server")
os.remove("Server.spec")

try:
    shutil.rmtree("build")

except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

try:
    shutil.rmtree("dist")

except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
