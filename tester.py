from launcher import tester

import config

output_files = 'results2'

config.citizen_source = 'citizens_old.txt'
config.links_source = 'links.txt'

runtime = 365

if __name__ == '__main__':
    tester(output_files, runtime)