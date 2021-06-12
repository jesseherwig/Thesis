from launcher import tester

import config

output_files = '1mil_80_1'

config.citizen_source = 'citizens.txt'
config.links_source = 'links_parallel.txt'

runtime = 80

if __name__ == '__main__':
    tester(output_files, runtime)