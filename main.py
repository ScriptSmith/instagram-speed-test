import random
import time

import runner.programs

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

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

doc_ref = db.collection('times').document(str(current_time))
doc_ref.set(appendage)
