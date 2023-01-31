import numpy as np
import random
import matplotlib.pyplot as plt

#funkcja ewaluacyjna lotu rakiety opisana w poleceniu zadania, do funkcji w argumencie podajemy tablice (w założeniu zadania 200 elementową) bitów symbolizujących stan włączenia silnika w danym momencie czasu. Funkcja ta oblicza ilość punktów jaki otrzymuje lot na podstawie podanego schematu włączania silnika zgodnie z zasadami podanymi w poleceniu ćwiczenia – tzn. w każdej jednostce czasu obliczane jest przyśpieszenie na podstawie pozostałej masy rakiety i wzorów z polecenia, a następnie zmieniana jest aktualna wysokość rakiety na podstawie wzoru na ruch jednostajnie przyśpieszony
def flightTotheMoon(individual):
    height = 0
    fuelInSum = sum(individual)
    rocketMass = 20 + fuelInSum
    velocity = 0
    for isEngineOn in individual:
        
        acceleration = isEngineOn*500/rocketMass - 0.9 - 0.06*velocity*abs(velocity)/rocketMass
        height = height+ velocity + acceleration/2
        velocity = velocity + acceleration
        rocketMass =rocketMass-1*isEngineOn

    if(height>750):
        return 200 - fuelInSum
    else:
        return 0
        
#funkcja tworząca losową tablice osobników w ilości “size” o rozmiarze bitów czasu w ilości „time”. Funkcja ta tworzy pierwszą populacje. Jako że bit każdego czasu jest dwuwymiarowy tj. symbolizuje albo wyłączony albo włączony silnik w jednostce czasu, to losując jego wartość z tym samym rozkładem prawdopodobieństwa za każdym razem, to prawdopodobieństwo wylosowania każdego stanu bitu wynosi ostatecznie 50%, przez co w większej próbce (w tym przypadku 200) wylosowana suma wartości jednego osobnika będzie oscylować wokół wartości 100 (ponieważ losowanie będzie dążyło do 50% ilości wszystkich bitów w wartości 0 i 50% w wartości 1)
def initializationOfTheFirstPopulation(size,time):
    return [[random.randint(0, 1) for i in range(time)] for j in range(size)]

#funkcja inicjująca selekcję ruletkową podanej w argumencie populacji (pop). Jako że algorytm genetyczny jest przystosowany do działania dla różnych funkcji ewaluacyjnych, to argumentem funkcji jest również referencja na funkcje zwracającą wartość na podstawie której maximum jest szukana. Funkcja ruletkowa działa na zasadzie przydzielania prawdopodobieństwa do każdej wartości osobnika na podstawie funkcji ewaluacyjnej. Wartość funkcji jest podzielona przez sumę wszystkich wartości funkcji z osobników populacji, po czym wartości na podstawie losowania i ich prawdopodobieństw są wybierane jako te najlepsze z danej populacji dopuszczone do reprodukcji.
def selectingIndividualsToReproduceByRoullete(pop,functionToOptimalize):

    scoreOfThePopulation = [functionToOptimalize(pop[i]) for i in range(len(pop))]

    probabilityOfIndividualInPopulation = [scoreOfThePopulation[i]/sum(scoreOfThePopulation) for i in range(len(scoreOfThePopulation))]

    selectedPopulation = np.random.default_rng().choice(pop, len(pop), p=probabilityOfIndividualInPopulation)
    return selectedPopulation

#funkcja która dzieli wyselekcjonowaną populacje (selectedPopulation) w pary, I później każda para ma prawdopodobieństwo na reprodukcje (probabiltyOfReproduce). Jeżeli reprodukcja nie zachodzi, para przechodzi do następnej generacji, a jeśli zachodzi to losowany jest punkt skrzyżowania i od tego punktu dwoje rodziców tworzy dwoje dzieci które mają zamienione od tego miejsca bity względem siebie. Następnie osobniki mają szanse na mutacje, a więc każdy bit osobników ma szanse na bycie bitem odwrotnym na podstawie prawdopodobieństwa na mutację (probabilityOfMutation). Następnie dzieci z reprodukcji zastępują swoich rodziców w populacji następnej generacji.
def singlePointCrossoverWithCertainPairsAndMutationOfChildren(selectedPopulation,probabiltyOfReproduce,probabilityOfMutation):
    
    
    for j in range(0,int(len(selectedPopulation)/2)*2,2):
        if(random.uniform(0, 1)<=probabiltyOfReproduce):
            selectedCrossPoint = random.randrange(len(selectedPopulation[j]))
            for k in range(selectedCrossPoint,len(selectedPopulation[j])):
                temp = selectedPopulation[j][k]
                selectedPopulation[j][k] = selectedPopulation[j+1][k]
                selectedPopulation[j+1][k] = temp
            
    for j in range(len(selectedPopulation)):
        for k in range(len(selectedPopulation[j])):
            if(random.uniform(0, 1)<=probabilityOfMutation):
                selectedPopulation[j][k] = selectedPopulation[j][k]*(-1) +1
                
    return selectedPopulation
    



timeStepAmount = 200 #ilosc bitów w jednym osobniku
functionToOptimalize = flightTotheMoon #wybor funkcji ewaluacyjnej

'''
#Sztywno narzucone hiperparametry algorytmu w celu otrzymania optymalnych wartosci maksymalizacji funkcji.
sizeOfPopulation = 150 #rozmiar populacji
amountOfGenerations = 150 #ilosc pokolen

probabilityOfMutation = 0.01 #prawdopodobienstwo mutacji genu
probabiltyOfReproduce = 0.75 #prawdopodobienstwo reprodukcji wyselekcjonowanej pary
'''

#Interfejs uzytkownika majacy na celu dobranie sobie wlasnych parametrow do pojedynczego ukonczenia algorytmu genetycznego
print("Podaj ilosc osobnikow na jedna populacje: ")
sizeOfPopulation = int(input())
print("Podaj ilosc generacji jaka ma zostac wykonana: ")
amountOfGenerations = int(input())
print("Podaj prawdopodobienstwo na to iz wyselekcjonowana para bedzie sie reprodukowac: ")
probabilityOfMutation = float(input())
print("Podaj prawdopodobienstwo na mutacje genu: ")
probabiltyOfReproduce = float(input())



#Pojedyncze uruchomienie algorytmu genetycznego dla narzuconych na sztywno parametrow lub wpisanych przez urzytkownika parametrow
population = initializationOfTheFirstPopulation(sizeOfPopulation,timeStepAmount) #inicjalizacja pierwszej populacji
selectedPopulation = population
biggestScore=0

for i in range(amountOfGenerations):
    selectedPopulation = selectingIndividualsToReproduceByRoullete(selectedPopulation,functionToOptimalize) #selekcja ruletkowa populacji
    selectedPopulation = singlePointCrossoverWithCertainPairsAndMutationOfChildren(selectedPopulation,probabiltyOfReproduce,probabilityOfMutation) #reprodukcja z mutacja populacji
    maxInGeneration = max([functionToOptimalize(selectedPopulation[i]) for i in range(len(selectedPopulation))]) #z danej populacji wyciagane jest maximum
    print("Najwiekszy z tej generacji to: " + str(maxInGeneration))
    if biggestScore < maxInGeneration:
        biggestScore = maxInGeneration #wyznaczanie maksimum z wszystkich generacji
            
print("Najwiekszy wynik otrzymany na przebiegu dziejow to: " + str(biggestScore))

'''
#Wielokrotne skorzystanie z algorytmu w celu przesledzenia wyników dla roznych hiperparametrow i zapisanie ich w pliku tekstowym data.txt w formacie [Rozmiar populacji; Ilosc generacji; P. mutacji; P. rozmnazania; Max funkcji z wszystkich pokolen; Wszystkie maksima wynikow populacji z każdej generacji; Wszystkie srednie wynikow populacji kazdej generacji]
sizeOfPopulationG = [100,200,300,500]
amountOfGenerationsG = [10,25,100,300]

probabilityOfMutationG = [0,0.001,0.01,0.05,0.1,0.5,1]
probabiltyOfReproduceG = [0.5,0.75,0.9,1]

with open('data.txt', 'w') as f:
    for sizeOfPopulation in sizeOfPopulationG:
        for amountOfGenerations in amountOfGenerationsG:
            for probabilityOfMutation in probabilityOfMutationG:
                for probabiltyOfReproduce in probabiltyOfReproduceG:
                    population = initializationOfTheFirstPopulation(sizeOfPopulation,timeStepAmount)
                    selectedPopulation = population
                    biggestScore=0
                    maxesOfGenerations = []
                    meansOfGenerations = []
                    
                    for i in range(amountOfGenerations):
                        selectedPopulation = selectingIndividualsToReproduceByRoullete(selectedPopulation,functionToOptimalize)
                        selectedPopulation = singlePointCrossoverWithCertainPairsAndMutationOfChildren(selectedPopulation,probabiltyOfReproduce,probabilityOfMutation)
                        scoresOfGenerations = [functionToOptimalize(selectedPopulation[i]) for i in range(len(selectedPopulation))]
                        maxInGeneration = max(scoresOfGenerations)
                        maxesOfGenerations.append(max(scoresOfGenerations))
                        meansOfGenerations.append(sum(scoresOfGenerations)/len(scoresOfGenerations))
                        if biggestScore < maxInGeneration:
                            biggestScore = maxInGeneration
                                
                    print(str(sizeOfPopulation) + " " + str(amountOfGenerations) + " " + str(probabilityOfMutation) + " " + str(probabiltyOfReproduce) + " " + str(biggestScore))        
                    f.write(str(sizeOfPopulation) + " " + str(amountOfGenerations) + " " + str(probabilityOfMutation) + " " + str(probabiltyOfReproduce) + " " + str(biggestScore) + " S " + str(maxesOfGenerations)+ " M " + str(meansOfGenerations) + "\n")
'''