import config

def chain(*lists):
    for alist in lists:
        for element in alist:
            yield element


from random import sample, choice, choices, randrange
from random import random as rand



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
        self.isolation_date = None
        self.forwardLinks = []
        self.backLinks = []
        self.toIsolate = False
        self.unisolating = False
        self.unisolatedState = None
        self.chance = 0.05

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
        self.unisolatedState = self.state

    def isolateContacts(self):
        for link in self.forwardLinks:
            if link.weight > 0.5:
                dest: Citizen = link.getDestination()
                dest.isolate()

    def isUnisolating(self):
        return self.unisolating

    def unisolationHelper(self, link, citizen):
        if not citizen.isUnisolating():
            if citizen.getIsolation_date() == self.isolation_date:
                link.setStatus(True)
                citizen.unisolate()

    def unisolate(self):
        self.unisolating = True
        for link in self.forwardLinks:
            dest: Citizen = link.getDestination()
            self.unisolationHelper(link, dest)
        for link in self.backLinks:
            source: Citizen = link.getSource()
            self.unisolationHelper(link, source)

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
        elif self.unisolating:
            self.state = self.unisolatedState
            self.unisolating = False
        method = getattr(self, self.state)
        return method()

    def susceptible(self):
        pass

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
        if rand() < self.age * 0.01 * config.parameters['hospitalisationFactor']:
            self.state = 'hospitalised'
            self.isolateContacts()
        elif rand() < self.age * 0.01 * config.parameters['deathFactor']:
            self.death()
        if config.day - self.infection_date > config.parameters['standardRecovery'] and rand() < self.chance:
            self.state = 'recovered'
        return self.state

    def hospitalised(self):
        from random import random as rand
        if rand() < self.age * 0.01 * config.parameters['deathFactor']:  # roll for death
            if rand() > self.immunity:  # Vaccinated
                self.state = 'deceased'
                self.death()
        elif config.day - self.infection_date > config.parameters['hospitalisedRecovery'] and rand() < self.chance:
            self.state = 'recovered'
        else:
            self.chance += 0.01
        return self.state

    def isolated(self):
        if config.day - self.isolation_date >= config.parameters['isolationTime']:
            self.unisolate()
            self.state = self.unisolatedState
        return self.state

    def recovered(self):
        pass

    def deceased(self):
        pass

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
        else: return False




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
            if self.destination.getState() == 'susceptible':
                immunityFactor = self.destination.getImmunity()
                mitigationFactor = self.source.getMitigationFactor()

                if rand() < self.weight:
                    if rand() > immunityFactor:
                        if rand() > mitigationFactor:
                            self.destination.infect(chance or None)
                            return self.destination
        return None



def select_vaccine(citizen: Citizen):
    age = citizen.getAge()
    if age >= 50:
        return choices(('astraZeneca', 'pfizer', 'moderna'), weights=[10, 1, 1], k=1)
    else:
        return choices(('pfizer', 'moderna'), weights=[51, 50], k=1)


class Population:

    def __init__(self):
        self.citizens = []
        self.links = []
        self.infected = []
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
        self.vaccine_totals = {
            'astraZeneca_half': 0,
            'astraZeneca_full': 0,
            'pfizer_half': 0,
            'pfizer_full': 0,
            'moderna_half': 0,
            'moderna_full': 0,
        }

    def load_sample(self):

        with open('citizens.txt', 'r') as f:
            print('load citizens')
            lines = f.readlines()
            for line in lines:
                if line != '':
                    line = line.strip()
                    (sex, age) = line.split(',')
                    self.addCitizen(Citizen(int(age), sex))
            f.close()
        print('done')
        with open('links_parallel.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line != '':
                    line = line.strip()
                    print(line)
                    (source, destination, weight) = line.split(',')
                    self.addLink(Link(self.citizens[int(source)],self.citizens[int(destination)], float(weight)))
        print('Done links')

    def addCitizen(self, citizen: Citizen):
        self.citizens.append(citizen)
        self.map[citizen.getState()].append(citizen)
        self.vaccinated['none'].append(citizen)

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
            self.infected.append(citizen)
            self.map['incubating'].append(citizen)
            citizen.infect()

    def advanceTime(self):
        for citizen in self.infected:
            old_state = citizen.getState()
            if old_state == 'contagious':
                for link in citizen.getForwardLinks():
                    if link.rollInfection():
                        infectee: Citizen = link.getDestination()
                        self.infected.append(infectee)
                        self.map['incubating'].append(infectee)
                        self.map['susceptible'].remove(infectee)
            citizen.advanceInfection()
            state = citizen.getState()
            if old_state != state:
                self.map[old_state].remove(citizen)
                self.map[state].append(citizen)
            if state == 'recovered' or state == 'deceased':
                self.infected.remove(citizen)

        ## Vaccinations
        for citizen in self.vaccinated['half']:
            if citizen.advanceVaccine():
                vac = citizen.getVaccine()
                self.vaccinated['half'].remove(citizen)
                self.vaccinated['full'].append(citizen)
                self.vaccine_totals[vac + '_half'] -= 1
                self.vaccine_totals[vac + '_full'] += 1

        try:
            toVaccinate = sample(self.vaccinated['none'], config.parameters['daily_vac_number'])
        except ValueError:
            toVaccinate = self.vaccinated['none'].copy()
        for citizen in toVaccinate:
            vac = select_vaccine(citizen)
            citizen.vaccinate(vac[0])
            self.vaccinated['none'].remove(citizen)
            self.vaccinated['half'].append(citizen)
            self.vaccine_totals[vac[0] + '_half'] += 1

        #Testing
        toTest = sample(self.citizens, randrange(config.parameters['tests']['min'], config.parameters['tests']['max']))
        for citizen in toTest:
            state = citizen.getState()
            if state in ['contagious', 'incubating']:
                citizen.isolate()
                citizen.isolateContacts()
                self.map[state].remove(citizen)
                citizen.setState('isolated')
                self.map['isolated'].append(citizen)
        if rand() < 0.05:
            citizen = choice(self.map['susceptible'])
            if citizen.rollInfection():
                self.map['susceptible'].remove(citizen)
                self.map['incubating'].append(citizen)
                self.infected.append(citizen)


    def print_stats(self):
        print('Day: ', config.day)
        print('Citizens: ', len(self.citizens))
        print('Total Infections: ', len(self.infected))
        print('-----States-----')
        print('Susceptible: ', len(self.map['susceptible']))
        print('Incubating: ', len(self.map['incubating']))
        print('Contagious: ', len(self.map['contagious']))
        print('Recovered: ', len(self.map['recovered']))
        print('Deceased: ', len(self.map['deceased']))
        print('Hospitalised: ', len(self.map['hospitalised']))
        print('Isolated: ', len(self.map['isolated']))
        print('Vaccines: ')
        print('-------------------------------')

    def string_stats(self):
        stats = '\nDay: ' + str(config.day) + '\nCitizens: ' \
                + str(len(self.citizens)) + '\nTotal Infections: ' + str(len(self.infected) + len(self.map['recovered']) + len(self.map['deceased'])) \
                + '\n-----States-----' + '\nSusceptible: ' + str(len(self.map['susceptible'])) \
                + '\nIncubating: ' + str(len(self.map['incubating'])) + '\nContagious: ' \
                + str(len(self.map['contagious'])) + '\nRecovered: ' + str(len(self.map['recovered'])) \
                + '\nDeceased: ' + str(len(self.map['deceased'])) + '\nHospitalised: ' \
                + str(len(self.map['hospitalised'])) + '\nIsolated:  ' \
                + str(len(self.map['isolated'])) \
                + '\n-------------------------------' \
                + '\nVaccines:\nAstraZeneca: \nHalf: ' + str(self.vaccine_totals['astraZeneca_half']) \
                + '  Full: ' + str(self.vaccine_totals['astraZeneca_full']) \
                + '\nPfizer: \nHalf: ' + str(self.vaccine_totals['pfizer_half']) \
                + '  Full: ' + str(self.vaccine_totals['pfizer_full']) \
                + '\nModerna: \nHalf: ' + str(self.vaccine_totals['moderna_half']) \
                + '  Full: ' + str(self.vaccine_totals['moderna_full']) \
                + '\n-------------------------------'
        return stats


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
