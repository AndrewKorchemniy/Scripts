import subprocess

install_dependancies = ["python", "-m", "pip", "install", "--upgrade",
                        "pip",
                        "click",
                        "appdirs",
                        "psutil",
                        "cloudscraper"]

subprocess.run(install_dependancies)
