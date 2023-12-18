import psutil
import subprocess

if not any(proc.name() == 'pwsh.exe' for proc in psutil.process_iter()):
    subprocess.run("pwsh.exe")
