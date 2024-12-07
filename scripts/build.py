import subprocess


def build():
    subprocess.run("black .", check=True, shell=True)
    subprocess.run("isort .", check=True, shell=True)
    subprocess.run("pytest --cov=blood_moon .", check=True, shell=True)


def blood_moon():
    subprocess.run(
        "python blood_moon/bm.py --run-if-blood-moon-phase", check=True, shell=True
    )
