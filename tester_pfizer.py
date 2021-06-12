from launcher import tester

import config

import os

output_files = '100k_all_pfizer'


config.citizen_source = 'citizens_100k_vaccinated_pfizer.txt'
config.links_source = 'links_100k.txt'
runtime = 365

if __name__ == '__main__':
    if os.path.exists(output_files + 'count.txt'):
        with open(output_files + 'count.txt', 'r') as f:
            count = int(f.read())
        count += 1
    else:
        count = 1
    with open(output_files + 'count.txt', 'w') as f:
        f.write(str(count))
    output_files += str(count)
    tester(output_files, runtime)
