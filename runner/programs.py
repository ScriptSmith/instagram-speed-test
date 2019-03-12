import os
import subprocess
import time
from typing import List


class Program:
    name: str = ""
    setup_commands: List[str] = []
    test_commands: List[str] = []

    def __init__(self, setup_commands: List[str], test_commands: List[str]):
        output_dir = ["cd output"]

        self.setup_commands = output_dir + setup_commands
        self.test_commands = output_dir + test_commands

    def setup(self):
        commands = " && ".join(self.setup_commands)
        self.subprocess_cmd(commands, print_output=False)

    def test(self):
        commands = " && ".join(self.test_commands)

        start_time = time.time()
        retcode = self.subprocess_cmd(commands, print_output=True)
        stop_time = time.time()

        duration = stop_time - start_time
        print(f"Execution of {self.name} took {duration} seconds")

        return int(duration) if retcode == 0 else -1



    @staticmethod
    def subprocess_cmd(commands: str, print_output: bool):
        print(f"COMMANDS: {commands}")
        if os.environ.get('PRINT_COMMANDS'):
            return

        process = subprocess.Popen(commands, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        comm = process.communicate()
        proc_stdout = comm[0].strip()
        proc_stderr = comm[1].strip()

        print(f"Exited with code {process.returncode}")

        if print_output or process.returncode != 0:
            print(proc_stdout.decode('utf-8'))
            print(proc_stderr.decode('utf-8'))

        return process.returncode


class PipProgram(Program):
    def __init__(self, setup_commands: List[str], test_commands: List[str]):
        venv_name = f"{self.name}_venv"
        pip_setup = [
            f"python3 -m venv {venv_name}",
            f". {venv_name}/bin/activate",
        ]
        pip_test = [
            f". {venv_name}/bin/activate"
        ]

        super().__init__(pip_setup + setup_commands, pip_test + test_commands)


class Instamancer(Program):
    def __init__(self):
        self.name = "instamancer"
        super().__init__(
            ["npm install -g instamancer"],
            ["instamancer hashtag selfie --count=500 -f=/dev/null"]
        )


class Instaphyte(PipProgram):
    def __init__(self):
        self.name = "instaphyte"
        super().__init__(
            ["pip install instaphyte"],
            ["instaphyte hashtag selfie --count=500 -f=/dev/null"]
        )


class Instaloader(PipProgram):
    def __init__(self):
        self.name = "instaloader"
        super().__init__(
            ["pip install instaloader"],
            ["instaloader '#selfie' --no-pictures -V -c 500"]
        )


class Instalooter(PipProgram):
    def __init__(self):
        self.name = "instalooter"
        super().__init__(
            ["pip install instalooter --pre"],
            ["instalooter hashtag selfie -n 500 -D"]
        )


class InstagramScraper(PipProgram):
    def __init__(self):
        self.name = "instagram-scraper"

        username = os.environ.get('INSTAGRAM_USER')
        password = os.environ.get('INSTAGRAM_PASS')
        test_command = "instagram-scraper selfie --tag --maximum=500" + \
                       f" -u {username} -p {password}"

        super().__init__(
            ["pip install instagram-scraper"],
            [test_command]
        )
