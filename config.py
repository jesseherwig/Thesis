parameters = {
    'size': 1000000,
    'hospitalisationFactor' : 0.1,
    'deathFactor': 0.1 ,
    'globalInfectionFactor': 1,
    'standardRecovery': 14,
    'contagiousTime': 7,
    'hospitalisedRecovery': 19,
    'isolationTime': 14,
    'daily_vac_number': 10,
    'tests': {'max': 3 ,
              'min': 1,
              'extreme_max': 100},
    'r': {'min': 2,
         'max': 6}
}
vaccines = {'astraZeneca_half': 0.641,
            'astraZeneca_full': 0.704,
            'pfizer_half': 0.52,
            'pfizer_full': 0.95,
            'moderna_half': 0.61,
            'moderna_full':0.945}
dose_space = {'astraZeneca': 90,
              'pfizer': 21,
              'moderna': 21}

day = 1
