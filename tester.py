from launcher import tester

import config

output_files = '50_all_az'

config.citizen_source = 'citizens_10k_vaccinated_az.txt'
config.links_source = 'links_1000.txt'
runtime = 365

if __name__ == '__main__':
    tester(output_files, runtime)
