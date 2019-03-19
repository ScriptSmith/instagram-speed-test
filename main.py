import random
import time

import runner.programs
from runner.items import items

import requests
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()
bucket = storage.bucket("instagram-speed-test.appspot.com")

programs = [
    runner.programs.Instamancer(),
    runner.programs.Instaphyte(),
    runner.programs.Instaloader(),
    runner.programs.Instalooter(),
    runner.programs.InstagramScraper(),
]

random.shuffle(programs)

current_time = int(time.time())

appendage = {}

for program in programs:
    program.setup()
    duration = program.test()

    appendage[program.name] = duration

    data = requests.get(
        f"https://img.shields.io/badge/{round(items / duration, 2)} "
        f"posts%2Fsecond-brightgreen.svg")

    blob = bucket.blob(program.name + ".svg")
    blob.upload_from_string(data.text, content_type="image/svg+xml")

doc_ref = db.collection('times').document(str(current_time))
doc_ref.set(appendage)

print("UPLOADED RESULTS")
