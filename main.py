import json
import random
import time

import runner.programs

programs = [
    runner.programs.Instamancer(),
    runner.programs.Instaphyte(),
    runner.programs.Instaloader(),
    runner.programs.Instalooter(),
    runner.programs.InstagramScraper(),
]

# random.shuffle(programs)

current_time = int(time.time())

appendage = {}

for program in programs:
    program.setup()
    duration = program.test()

    appendage[program.name] = duration

with open("data.json", "r+") as f:
    data = f.read()

    json_data = json.loads(data)
    json_data[current_time] = appendage

    f.seek(0)
    f.write(json.dumps(json_data))
    f.truncate()

