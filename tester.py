from launcher import tester

import config

output_files = '1mil_365'

config.citizen_source = 'citizens.txt'
config.links_source = 'links_parallel.txt'
runtime = 365

if __name__ == '__main__':
    tester(output_files, runtime)