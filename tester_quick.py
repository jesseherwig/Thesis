from launcher import tester

import config

output_files = '50k_365'

config.citizen_source = 'citizens_50k.txt'
config.links_source = 'links_50k.txt'

runtime = 80

if __name__ == '__main__':
    tester(output_files, runtime)