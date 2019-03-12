import os
import subprocess
import time
from typing import List


class Program:
    name: str = ""
    setup_commands: List[str] = []
    test_commands: List[str] = []

    def __init__(self, setup_commands: List[str], test_commands: List[str]):
        self.setup_commands = setup_commands
        self.test_commands = test_commands

    def setup(self):
        commands = " && ".join(self.setup_commands)
        self.subprocess_cmd(commands, print_output=True)

    def test(self):
        commands = " && ".join(self.test_commands)

        start_time = time.time()
        self.subprocess_cmd(commands, print_output=True)
        stop_time = time.time()

        duration = stop_time - start_time
        print(f"Execution of {self.name} took {duration} seconds")

    @staticmethod
    def subprocess_cmd(commands: str, print_output: bool):
        print(f"COMMANDS: {commands}")
        if os.environ.get('PRINT_COMMANDS'):
            return

        process = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()

        if print_output:
            print(proc_stdout)


class PipProgram(Program):
    def __init__(self, setup_commands: List[str], test_commands: List[str]):
        venv_name = f"{self.name}_venv"
        pip_setup = [
            f"python3 -m venv {venv_name}",
            f". {venv_name}/bin/activate",
            "which pip"
        ]
        pip_test = [
            f". {venv_name}/bin/activate"
        ]

        super().__init__(pip_setup + setup_commands, pip_test + test_commands)


class Instamancer(Program):
    def __init__(self):
        self.name = "instamancer"
        super().__init__(
            ["sudo npm install -g instamancer"],
            ["instamancer hashtag selfie --count=100 -f=/dev/null'"]
        )


class Instaphyte(PipProgram):
    def __init__(self):
        self.name = "instaphyte"
        super().__init__(
            ["pip install instaphyte"],
            ["instaphyte hashtag selfie --count=100 -f=/dev/null"]
        )


class Instaloader(PipProgram):
    def __init__(self):
        self.name = "instaloader"
        super().__init__(
            ["pip install instaloader"],
            ["instaloader '#selfie' --no-pictures -V -c 100"]
        )
