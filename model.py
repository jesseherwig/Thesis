import csv

import config

import multiprocessing as mp



from random import sample, choice, choices, randrange
from random import random as rand


def try_death(age,sex):
    if age < 60:
        i = '<60'
    elif age >= 80:
        i = '80+'
    else:
        if age < 70:
            i = '60-69'
        else:
            i = '70-79'
    if rand() < config.parameters['deathFactor'][sex][i]:
        return True
    else:
        return False

def try_hospital(age):
    if age < 5:
        i = '0-4'
    elif age >= 65:
        i = '65+'
    elif age < 18:
        i = '5-17'
    elif age < 50:
        i = '18-49'
    else:
        i = '50-64'
    if rand() < config.parameters['hospitalisationFactor'][i]/100000:
        return True
    else:
        return False


class Citizen:

    def __init__(self, age, sex, state=None, vaccine=None, immunity=None, mitigationFactor=None, infection_date=None):
        self.state = state or 'susceptible'
        self.age = age
        self.sex = sex
        self.immunity = immunity or 0
        self.vaccine = vaccine or 'none'
        self.mitigationFactor = mitigationFactor or 0
        self.infection_date = infection_date or None
        self.vaccination_date = None
        if vaccine:
            self.vaccination_date = config.dose_space[vaccine]
            self.immunity = config.vaccines[vaccine + '_full']
        self.isolation_date = None
        self.forwardLinks = []
        self.backLinks = []
        self.toIsolate = False
        self.unisolatedState = None
        self.chance = 0.05
        self.max_infected = randrange(config.parameters['r']['min'], config.parameters['r']['max'])
        self.num_infected = 0

    def addForwardLink(self, link):
        assert isinstance(link, Link)
        self.forwardLinks.append(link)

    def removeForwardLink(self, link):
        if link in self.forwardLinks:
            assert isinstance(link, Link)
            self.forwardLinks.remove(link)
            return True
        else:
            return False

    def addBackLink(self, link):
        assert isinstance(link, Link)
        self.backLinks.append(link)

    def removeBackLink(self, link):
        if link in self.backLinks:
            assert isinstance(link, Link)
            self.backLinks.remove(link)
            return True
        else:
            return False

    def getForwardLinks(self):
        return self.forwardLinks

    def check_max_not_exceeded(self):
        if self.num_infected > self.max_infected:
            return False
        else:
            return True

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setAge(self, age):
        self.age = age

    def getAge(self):
        return self.age

    def setSex(self, sex):
        self.sex = sex

    def getSex(self):
        return self.sex

    def setVaccine(self, vaccine):
        self.vaccine = vaccine

    def getVaccine(self):
        return self.vaccine

    def setImmunity(self, immunity):
        self.immunity = immunity

    def getImmunity(self):
        return self.immunity

    def setMitigationFactor(self, mitigation):
        self.mitigationFactor = mitigation

    def getMitigationFactor(self):
        return self.mitigationFactor

    def setTimeSinceInfection(self, time):
        self.infection_date = time

    def getTimeSinceInfection(self):
        return self.infection_date

    def getIsolation_date(self):
        return self.isolation_date or False

    def setMaxInfected(self, num):
        self.max_infected = num

    def increment_infected_num(self):
        self.num_infected += 1

    def infect(self, chance=None):
        if self.state == 'susceptible':
            self.state = 'incubating'
            self.chance = chance or 0.05
            self.infection_date = config.day

    def isolate(self):
        for link in self.forwardLinks:
            link.setStatus(False)
        for link in self.backLinks:
            link.setStatus(False)
        self.isolation_date = config.day
        if not self.unisolatedState:
            self.unisolatedState = self.state
        self.toIsolate = True

    def unisolate(self):
        for link in self.forwardLinks:
            dest: Citizen = link.getDestination()
            if dest.getState() != 'isolated':
                link.setStatus(True)
        for link in self.backLinks:
            source: Citizen = link.getSource()
            if source.getState() != 'isolated':
                link.setStatus(True)

    def isolateContacts(self):
        for link in self.forwardLinks:
            if link.weight > 0.5:
                dest: Citizen = link.getDestination()
                dest.isolate()

    def death(self):
        self.state = 'deceased'
        for link in self.forwardLinks:
            link.destroy()
        for link in self.backLinks:
            link.destroy()

    def advanceInfection(self):
        if self.toIsolate:
            self.state = 'isolated'
            self.toIsolate = False
            return self.state
        else:
            method = getattr(self, self.state)
            return method()

    def susceptible(self):
        return self.state

    def incubating(self):
        if config.day - self.infection_date == config.parameters['contagiousTime']:
            self.chance = 0.75

        from random import random as rand

        if rand() < self.chance:
            self.state = 'contagious'
        else:
            self.chance += 0.01
        if config.day - self.infection_date > config.parameters['standardRecovery'] and rand() < self.chance:
            self.state = 'recovered'
        return self.state

    def contagious(self):
        from random import random as rand
        if try_hospital(self.age):
            self.state = 'hospitalised'
            self.isolateContacts()
        elif try_death(self.age, self.sex):
            self.death()
        if config.day - self.infection_date > config.parameters['standardRecovery'] and rand() < self.chance:
            self.state = 'recovered'
        return self.state

    def hospitalised(self):
        from random import random as rand
        if try_death(self.age, self.sex):  # roll for death
            self.death()
        elif config.day - self.infection_date > config.parameters['hospitalisedRecovery'] and rand() < self.chance:
            self.state = 'recovered'
        else:
            self.chance += 0.01
        return self.state

    def isolated(self):
        if config.day - self.isolation_date >= config.parameters['isolationTime']:
            self.state = self.unisolatedState
            self.unisolate()
        return self.state

    def recovered(self):
        return self.state

    def deceased(self):
        return self.state

    def vaccinate(self, vaccine):
        self.vaccination_date = config.day
        self.immunity = config.vaccines[vaccine + '_half']
        self.vaccine = vaccine

    def advanceVaccine(self):
        if self.vaccination_date + config.dose_space[self.vaccine] == config.day:
            self.immunity = config.vaccines[self.vaccine + '_full']
            return True
        return False

    def rollInfection(self):
        if rand() > self.immunity:
            self.infect()
            return True
        else:
            return False


class Link:
    def __init__(self, source, destination, weight=None, status=None):
        self.source: Citizen = source
        self.destination: Citizen = destination
        self.source.addForwardLink(self)
        self.destination.addBackLink(self)
        self.weight = weight or 1
        self.status = status or True

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def destroy(self):
        self.source.removeForwardLink(self)
        self.destination.removeBackLink(self)

    def getSource(self):
        return self.source

    def getDestination(self):
        return self.destination

    def copy(self, source=None, destination=None, weight=None, status=None):
        clone = Link(source or self.source, destination or self.destination)
        if weight:
            clone.setWeight(weight)
        if status:
            clone.setStatus(status)
        return clone

    def rollInfection(self, chance=None):
        if self.status:
            state = self.destination.getState()
            if state == 'susceptible':
                immunityFactor = self.destination.getImmunity()
                mitigationFactor = self.source.getMitigationFactor()

                if rand() < self.weight:
                    if rand() > immunityFactor:
                        if rand() > mitigationFactor:
                            self.destination.infect(chance or None)
                            self.source.increment_infected_num()
                            return self.destination
        return None


def select_vaccine(citizen: Citizen):
    age = citizen.getAge()
    if age >= 50:
        return choices(('astraZeneca', 'pfizer', 'moderna'), weights=[10, 1, 1], k=1)
    else:
        return choices(('pfizer', 'moderna'), weights=[51, 50], k=1)

def load_citizens(line):
    if line != '':
        line = line.strip()
        sex, age, *vaccine = line.split(',')
        if vaccine:
            return Citizen(int(age), sex, vaccine=vaccine[0])
        else:
            return Citizen(int(age), sex)
    return None

def load_links(line):
    if line != '':
        line = line.strip()
        print(line)
        (source, destination, weight) = line.split(',')
        return [source, destination, weight]
    return None


class Population:

    def __init__(self):
        self.citizens = []
        self.links = []
        self.infected = 0
        self.vaccinated = {
            'none': [],
            'half': [],
            'full': []
        }
        self.map = {
            'incubating': [],
            'susceptible': [],
            'contagious': [],
            'hospitalised': [],
            'deceased': [],
            'recovered': [],
            'isolated': []
        }
        self.totals = {
            'incubating': 0,
            'susceptible': 0,
            'contagious': 0,
            'hospitalised': 0,
            'deceased': 0,
            'recovered': 0,
            'isolated': 0
        }
        self.vaccine_totals = {
            'astraZeneca_half': 0,
            'astraZeneca_full': 0,
            'pfizer_half': 0,
            'pfizer_full': 0,
            'moderna_half': 0,
            'moderna_full': 0,
        }
        self.last_infected = 0
        self.size = 0

    def load_sample(self):
        with mp.Pool(mp.cpu_count()) as p:
            print('load citizens')
            with open(config.citizen_source, 'r') as f:
                lines = f.readlines()
                f.close()
            citizens = p.map(load_citizens, lines)
            self.size = len(citizens)
            self.addCitizenList(citizens)
            print('done')
            p.close()
            p.join()
        with open(config.links_source, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line != '':
                    line = line.strip()
                    (source, destination, weight) = line.split(',')
                    self.addLink(Link(self.citizens[int(source)], self.citizens[int(destination)], float(weight)))
        print('Done links')
        superspreaders = sample(self.citizens, round(config.parameters['superspreaders'] / 100 * self.size))
        for citizen in superspreaders:
            citizen.setMaxInfected(len(citizen.getForwardLinks()))

    def addCitizen(self, citizen: Citizen):
        self.citizens.append(citizen)
        state = citizen.getState()
        self.map[state].append(citizen)
        self.totals[state] += 1
        try:
            self.vaccinated[citizen.getVaccine()].append(citizen)
        except KeyError:
            self.vaccinated['full'].append(citizen)
            self.vaccine_totals[citizen.getVaccine() + '_full'] += 1

    def addCitizenList(self, alist):
        for citizen in alist:
            self.addCitizen(citizen)

    def addLink(self, link):
        self.links.append(link)

    def addLinkList(self, alist):
        for link in alist:
            self.links.append(link)

    def setInfected(self, number):
        assert number >= 1
        from random import sample
        selected = sample(self.map['susceptible'], number)
        for citizen in selected:
            self.map['susceptible'].remove(citizen)
            self.map['incubating'].append(citizen)
            self.totals['incubating'] += 1
            self.totals['susceptible'] -= 1
            citizen.infect()
        self.infected += number

    def advanceTime(self):
        infected = 0
        for citizen in self.citizens:
            old_state = citizen.getState()
            if old_state == 'contagious' and citizen.check_max_not_exceeded():
                for link in citizen.getForwardLinks():
                    if link.rollInfection():
                        infectee: Citizen = link.getDestination()
                        self.infected += 1
                        self.map['incubating'].append(infectee)
                        self.map['susceptible'].remove(infectee)
                        self.totals['incubating'] += 1
                        self.totals['susceptible'] -= 1
                        infected += 1
                    if not citizen.check_max_not_exceeded() or rand() > 0.5:
                        break
            state = citizen.advanceInfection()
            if old_state != state:
                self.map[old_state].remove(citizen)
                self.map[state].append(citizen)
                if old_state != 'isolated' and state != 'isolated':
                    self.totals[old_state] -= 1
                    self.totals[state] += 1
            if state == 'recovered' or state == 'deceased':
                self.citizens.remove(citizen)

        ## Vaccinations
        for citizen in self.vaccinated['half']:
            if citizen.advanceVaccine():
                vac = citizen.getVaccine()
                self.vaccinated['half'].remove(citizen)
                self.vaccinated['full'].append(citizen)
                self.vaccine_totals[vac + '_half'] -= 1
                self.vaccine_totals[vac + '_full'] += 1

        try:
            toVaccinate = sample(self.vaccinated['none'], round(config.parameters['daily_vac_number']/100*self.size))
        except ValueError:
            toVaccinate = self.vaccinated['none'].copy()
        for citizen in toVaccinate:
            vac = select_vaccine(citizen)
            citizen.vaccinate(vac[0])
            self.vaccinated['none'].remove(citizen)
            self.vaccinated['half'].append(citizen)
            self.vaccine_totals[vac[0] + '_half'] += 1

        # Testing
        testNumber = int((randrange(config.parameters['tests']['min'], config.parameters['tests']['max'])/100 * self.size) \
                     + round(self.last_infected * (self.size / 100)))
        if testNumber > config.parameters['tests']['extreme_max']/100 * self.size:
            testNumber = int(config.parameters['tests']['extreme_max']/100 * self.size)
        self.last_infected = infected
        toTest = sample(self.citizens, testNumber)
        for citizen in toTest:
            state = citizen.getState()
            if state in ['contagious', 'incubating']:
                citizen.isolate()
                citizen.isolateContacts()
                self.map[state].remove(citizen)
                citizen.setState('isolated')
                self.map['isolated'].append(citizen)
        if rand() < 0.05 and len(self.map['susceptible']) > 0:
            citizen = choice(self.map['susceptible'])
            if citizen.rollInfection():
                self.map['susceptible'].remove(citizen)
                self.map['incubating'].append(citizen)
                self.infected += 1
                self.totals['incubating'] += 1
                self.totals['susceptible'] -= 1

    def csv_stats(self, csv_path):
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([config.day, self.infected, self.totals['susceptible'],
                             self.totals['incubating'], self.totals['contagious'],
                             self.totals['recovered'], self.totals['deceased'],
                             self.totals['hospitalised'], len(self.map['isolated']),
                             self.vaccine_totals['astraZeneca_half'], self.vaccine_totals['astraZeneca_full'],
                             self.vaccine_totals['pfizer_half'], self.vaccine_totals['pfizer_full'],
                             self.vaccine_totals['moderna_half'], self.vaccine_totals['moderna_full']
                             ])

    def string_stats(self):
        stats = '\nDay: ' + str(config.day) + '\nCitizens: ' \
                + str(self.size) + '\nTotal Infections: ' + str(self.infected) \
                + '\n-----States-----' + '\nSusceptible: ' + str(self.totals['susceptible']) \
                + '\nIncubating: ' + str(self.totals['incubating']) + '\nContagious: ' \
                + str(self.totals['contagious']) + '\nRecovered: ' + str(self.totals['recovered']) \
                + '\nDeceased: ' + str(self.totals['deceased']) + '\nHospitalised: ' \
                + str(self.totals['hospitalised']) + '\n--Isolated: ' + str(len(self.map['isolated'])) \
                + ' --\n----Vaccines----' + '\nAstraZeneca: \nHalf: ' \
                + str(self.vaccine_totals['astraZeneca_half']) \
                + '  Full: ' + str(self.vaccine_totals['astraZeneca_full']) \
                + '\nPfizer: \nHalf: ' + str(self.vaccine_totals['pfizer_half']) \
                + '  Full: ' + str(self.vaccine_totals['pfizer_full']) \
                + '\nModerna: \nHalf: ' + str(self.vaccine_totals['moderna_half']) \
                + '  Full: ' + str(self.vaccine_totals['moderna_full']) \
                + '\n-------------------------------'
        return stats
