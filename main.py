import runner.programs

programs = [
    runner.programs.Instamancer(),
    runner.programs.Instaphyte(),
    runner.programs.Instaloader(),
    runner.programs.Instalooter(),
    runner.programs.InstagramScraper(),
]

for program in programs:
    program.setup()
    program.test()
