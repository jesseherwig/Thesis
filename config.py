parameters = {
    'size': 50000,
    'hospitalisationFactor': {
        '0-4': 0.3,
        '5-17': 0.1,
        '18-49': 2.5,
        '50-64': 7.4,
        '65+': 13.8,

    },
    'deathFactor': {
        'male': {'<60': 0.0000305,
                 '60-69': 0.0003865,
                 '70-79': 0.0012566,
                 '80+': 0.00475087},
        'female': {'<60': 0.0000139,
                   '60-69': 0.00015749,
                   '70-79': 0.00056988,
                   '80+': 0.00316181}
    },
    'r': {'min': 2,
          'max': 6},
    'standardRecovery': 14,
    'contagiousTime': 7,
    'hospitalisedRecovery': 19,
    'isolationTime': 14,
    'daily_vac_number': 0.4,
    'tests': dict(max=3, min=1, extreme_max=15),
    'superspreaders': 1
}
vaccines = {'astraZeneca_half': 0.641,
            'astraZeneca_full': 0.704,
            'pfizer_half': 0.52,
            'pfizer_full': 0.95,
            'moderna_half': 0.61,
            'moderna_full': 0.945}
dose_space = {'astraZeneca': 90,
              'pfizer': 21,
              'moderna': 21}

day = 0

citizen_source = 'citizens_50k_vaccinated_moderna.txt'
links_source = 'links_50k.txt'

generate_vaccine = 'moderna'
