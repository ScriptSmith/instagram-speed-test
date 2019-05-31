import random
import time
import json

import runner.programs
from runner.items import items

import requests
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred)

bucket = storage.bucket("instagram-speed-test.appspot.com")

speeds_blob = bucket.blob("speeds.json")
speeds = json.loads(speeds_blob.download_as_string())

programs = [
    runner.programs.Instamancer(),
    runner.programs.Instaphyte(),
    runner.programs.Instaloader(),
    runner.programs.Instalooter(),
    runner.programs.InstagramScraper(),
]

random.shuffle(programs)

current_time = int(time.time())

appendage = speeds['times'][str(current_time)] = {}

for program in programs:
    program.setup()
    duration = program.test()

    appendage[program.name] = duration

    url = f"https://img.shields.io/badge/speed-{round(items / duration, 2)}" \
        f" posts%2Fsecond-brightgreen.svg" if duration > 0 else \
        "https://img.shields.io/badge/-failed-red.svg"

    data = requests.get(url)

    blob = bucket.blob(program.name + ".svg")
    blob.upload_from_string(data.text, content_type="image/svg+xml")

speeds_blob.upload_from_string(json.dumps(speeds),
                               content_type="application/json")
print("UPLOADED RESULTS")
