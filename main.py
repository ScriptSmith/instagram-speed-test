import runner.programs

programs = [
    # runner.programs.Instamancer(),
    runner.programs.Instaphyte(),
    runner.programs.Instaloader(),
]

for program in programs:
    program.setup()
    program.test()
