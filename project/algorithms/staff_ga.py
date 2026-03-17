import random
import copy

POP_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.15
ELITISM_COUNT = 2

def initialize_population(doctors, patients):
    """Initialize random population"""
    population = []
    for _ in range(POP_SIZE):
        chromosome = []
        for patient in patients:
            suitable_doctors = [
                doc for doc in doctors 
                if doc["available"] and is_suitable(doc, patient)
            ]
            
            if suitable_doctors:
                chromosome.append(random.choice(suitable_doctors))
            else:
                available = [doc for doc in doctors if doc["available"]]
                chromosome.append(random.choice(available) if available else doctors[0])
        population.append(chromosome)
    return population

def is_suitable(doctor, patient):
    """Check if doctor is suitable for patient"""
    if patient["priority"] == "RED":
        return doctor["skill"] == "ICU"
    elif patient["ward"] == "ICU":
        return doctor["skill"] in ["ICU", "General"]
    else:
        return doctor["skill"] in ["Ward", "General"]

def fitness(chromosome, patients):
    """Calculate fitness score"""
    score = 0
    doctor_load = {}
    doctor_specialty = {}
    
    for gene, patient in zip(chromosome, patients):
        if patient["priority"] == "RED" and gene["skill"] == "ICU":
            score += 50
        elif gene["skill"] == patient["ward"]:
            score += 30
        elif gene["skill"] == "General" and patient["ward"] in ["ICU", "Ward"]:
            score += 20
        else:
            score += 5
        
        doctor_load[gene["name"]] = doctor_load.get(gene["name"], 0) + 1
        doctor_specialty[gene["name"]] = gene["skill"]
    
    avg_load = len(patients) / len(set([d["name"] for d in chromosome]))
    
    for name, load in doctor_load.items():
        if load > avg_load * 1.5:  
            score -= 20 * (load - avg_load)
        elif load < avg_load * 0.5:  
            score -= 10
    
    specialties = set(doctor_specialty.values())
    if len(specialties) > 1:
        score += len(specialties) * 5
    
    return max(score, 1)  

def crossover(parent1, parent2):
    """Single-point crossover"""
    if len(parent1) <= 1:
        return parent1.copy()
    
    point = random.randint(1, len(parent1)-1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(chromosome, doctors):
    """Mutation operator"""
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            available_doctors = [doc for doc in doctors if doc["available"]]
            if available_doctors:
                chromosome[i] = random.choice(available_doctors)
    return chromosome

def selection(population, patients, tournament_size=3):
    """Tournament selection"""
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda c: fitness(c, patients), reverse=True)
    return tournament[0]

def genetic_algorithm(doctors, patients):
    """Main genetic algorithm"""
    if not doctors:
        return []
    
    population = initialize_population(doctors, patients)
    
    for generation in range(GENERATIONS):
        population.sort(key=lambda c: fitness(c, patients), reverse=True)
        
        next_gen = population[:ELITISM_COUNT]
        
        while len(next_gen) < POP_SIZE:
            parent1 = selection(population, patients)
            parent2 = selection(population, patients)
            
            child = crossover(parent1, parent2)
            
            child = mutate(child, doctors)
            
            next_gen.append(child)
        
        population = next_gen
    
    population.sort(key=lambda c: fitness(c, patients), reverse=True)
    return population[0]