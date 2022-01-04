import subprocess
import platform
import argparse
import os
from datetime import datetime
from decouple import config


if platform.system() != "Linux":
    exit("error: This can only run on Linux.")


try:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--service_name", help="Name of the service you want to create."
    )
    args = parser.parse_args()

    if not os.path.isdir(f'{config("WORKING_DIR")}/log/'):
        os.mkdir(f'{config("WORKING_DIR")}/log/')

    if not os.path.isfile(f'{config("WORKING_DIR")}/log/stdout.log'):
        with open(f'{config("WORKING_DIR")}/log/stdout.log', "w") as f:
            f.write(f"Created: {datetime.utcnow()}\n")

    if not os.path.isfile(f'{config("WORKING_DIR")}/log/stderr.log'):
        with open(f'{config("WORKING_DIR")}/log/stderr.log', "w") as f:
            f.write(f"Created: {datetime.utcnow()}\n")

    while True:
        subprocess.call(
            [
                "sudo",
                "python",
                "-m",
                "pip",
                "install",
                "--upgrade",
                "-r",
                "requirements.txt",
            ],
            shell=False,
        )
        break

    while True:
        subprocess.call(
            ["sudo", "addgroup", "--system", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.call(
            [
                "sudo",
                "adduser",
                "--system",
                "--no-create-home",
                "--disabled-login",
                "--disabled-password",
                "--ingroup",
                f"{args.service_name}",
                f"{args.service_name}",
            ],
            shell=False,
        )
        break

    while True:
        subprocess.call(
            ["sudo", "usermod", "-a", "-G", "sudo", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.call(
            ["sudo", "usermod", "-a", "-G", "video", f"{args.service_name}"],
            shell=False,
        )
        break

    while True:
        subprocess.call(
            ["sudo", "touch", f"/lib/systemd/system/{args.service_name}.service"],
            shell=False,
        )
        break

    service = f"""[Unit]
    Requires=network-online.target
    After=network-online.target
    StandardOutput=append:{config("WORKING_DIR")}/log/stdout.log
    StandardError=append:{config("WORKING_DIR")}/log/stderr.log
    Description="{args.service_name} Service"
    [Service]
    WorkingDirectory={config("WORKING_DIR")}
    ExecStart=/usr/bin/python {config("WORKING_DIR")}vision.py
    User={args.service_name}
    [Install]
    WantedBy=multi-user.target"""

    with open(f"/lib/systemd/system/{args.service_name}.service", "w") as f:
        f.write(service)

    while True:
        subprocess.call(
            ["sudo", "systemctl", "enable", f"{args.service_name}"], shell=False
        )
        break

    print("vision-2021 is installed and enabled. It will start on boot.")

except Exception as e:
    print("error: Please run as root. (sudo python setup.py)")
    print(e)
