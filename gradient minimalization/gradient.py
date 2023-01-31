#wykonal Tadeusz Golczyk, 300531
import numpy as np
import matplotlib.pyplot as plt
import random

def funkcjaF(x): #Funkcja zwracająca wartosc funkcji f na podstawie podanego punktu poczatkowego
    return pow(x,4)

def gradientF(x): #Funkcja zwracająca wartosc gradientu unkcji f na podstawie podanego punktu poczatkowego
    return 4*pow(x,3)


def funkcjaG(x): #Funkcja zwracająca wartosc funkcji g na podstawie podanych dwóch punktów poczatkowych
    return np.array(1.5 - np.exp(-pow(x[0],2)-pow(x[1],2)) - 0.5*np.exp(-pow(x[0]-1,2)-pow(x[1]+2,2)))

def gradientG(x): #Funkcja zwracająca wartosc gradientu funkcji g na podstawie podanych dwóch punktów poczatkowych
    return np.array([[2*x[0]*np.exp(-pow(x[0],2)-pow(x[1],2))+(x[0]-1)*np.exp(-np.exp(-pow(x[0]-1,2)-pow(x[1]+2,2)))],
                     [2*x[1]*np.exp(-pow(x[0],2)-pow(x[1],2))+(x[1]+2)*np.exp(-np.exp(-pow(x[0]-1,2)-pow(x[1]+2,2)))]])

def znajdowanieMinimum(x,b,funk,grad): #Funkcja zwracająca minimum fukncji podanej jako 3ci argument, na podstawie algorytmu gradientów. Należy podać również funkcje zwracającą wartosc gradientu funkcji oraz punkt poczatkowy dla algorytmu, oraz wspolczynnik kroku
    kroki = [np.array(x)]
    
    nastepnyP = np.squeeze(x - np.array(np.transpose(grad(np.array(x)))*b))
    kroki.append(nastepnyP)
    while funk(np.array(nastepnyP)) < funk(np.array(x)) and (abs(x - nastepnyP) > 0.00001).all() :
        #print(nastepnyP)
        x = nastepnyP
        nastepnyP = np.squeeze(x - np.array(np.transpose(grad(x))*b))
        kroki.append(nastepnyP)
    
    #print(nastepnyP)
    #print(kroki)
    return nastepnyP, kroki

def randomParePowtorzenFunkcjaF(startZakresX, koniecZakresX, iloscPowtorzen): #funkcja mająca na celu parokrotne powtórzenie procesu znajdowania minimum funkcji f ale dla kolejnych różniących się od siebie odrobine wartości współczynniku kroku oraz dla różnego losowego punktu początkowego od którego rozpoczniemy algorytm.
    minimumKrokuWspolczynnika = 0.0000001
    startWspolczynnika = 0
    koniecWspolczynnika = int(0.001/minimumKrokuWspolczynnika)
    
    with open('dataRandomF.txt', 'w') as f:
        for i in range(iloscPowtorzen):
            punktF = random.uniform(startZakresX, koniecZakresX)
            print(punktF)
            for wspK in range(startWspolczynnika,koniecWspolczynnika,50):
                minimumX, kolejneKrokiX = znajdowanieMinimum(punktF,wspK*minimumKrokuWspolczynnika, funkcjaF, gradientF)    
                f.write(str(punktF) + " " + str(wspK*minimumKrokuWspolczynnika) + " " + str(minimumX) + "\n")
                print(i, punktF,wspK*minimumKrokuWspolczynnika,minimumX)

def randomParePowtorzenFunkcjaG(startZakresX1, startZakresX2, koniecZakresX1, koniecZakresX2, iloscPowtorzen): #funkcja mająca na celu parokrotne powtórzenie procesu znajdowania minimum funkcji g ale dla kolejnych różniących się od siebie odrobine wartości współczynniku kroku oraz dla różnych losowych punktów początkowych od których rozpoczynamy algorytm.
    minimumKrokuWspolczynnika = 0.0000001
    startWspolczynnika = 0
    koniecWspolczynnika = int(0.001/minimumKrokuWspolczynnika)
    
    with open('dataRandomG.txt', 'w') as f:
        for i in range(iloscPowtorzen):
            punktG1 = random.uniform(startZakresX1, koniecZakresX1)
            punktG2 = random.uniform(startZakresX1, koniecZakresX1)
            print(punktG1,punktG2)
            for wspK in range(startWspolczynnika,koniecWspolczynnika,500):
                minimumX, kolejneKrokiX = znajdowanieMinimum([punktG1,punktG2],wspK*minimumKrokuWspolczynnika, funkcjaG, gradientG)   
                f.write(str(punktG1) + " " + str(punktG2) + " " + str(wspK*minimumKrokuWspolczynnika) + " " + str(minimumX) + "\n")
                print(i, punktG1,punktG2,wspK*minimumKrokuWspolczynnika,minimumX)

def randomParePowtorzenMenuF(): #interfejs użytkownika do wprowadzenia swoich danych wejściowych do funkcji randomParePowtorzenFunkcjaF
    print("Prosze wprowadzic rozpoczecie przedzialu losowego punktu poczatkowego funkcji f")
    start = float(input())
    print("Prosze wprowadzic koniec przedzialu losowego punktu poczatkowego funkcji f")
    koniec = float(input())
    print("Prosze wprowadzic ilosc powtorzen")
    amount = int(input())
    randomParePowtorzenFunkcjaF(start,koniec,amount)

def randomParePowtorzenMenuG(): #interfejs użytkownika do wprowadzenia swoich danych wejściowych do funkcji randomParePowtorzenFunkcjaG
    print("Prosze wprowadzic rozpoczecie przedzialu losowego pierwszego punktu poczatkowego funkcji g")
    start1 = float(input())
    print("Prosze wprowadzic koniec przedzialu losowego pierwszego punktu poczatkowego funkcji g")
    koniec1 = float(input())
    print("Prosze wprowadzic rozpoczecie przedzialu losowego drugiego punktu poczatkowego funkcji g")
    start2 = float(input())
    print("Prosze wprowadzic koniec przedzialu losowego drugiego punktu poczatkowego funkcji g")
    koniec2 = float(input())
    print("Prosze wprowadzic ilosc powtorzen")
    amount = int(input())
    randomParePowtorzenFunkcjaG(start1,start2,koniec1,koniec2,amount)

def pojedynczeFzWizualizacja(): #interfejs do jednorazowego znalezienia minimum funkcji f wraz z wizualizacją kolejnych kroków algorytmu
    print("Prosze wprowadzic punkt poczatkowy funkcji f")
    punktP= [float(input())]
    #punktP = [150]
    
    print("Prosze wprowadzic współczynnik długosci kroku beta")
    wspolczynnikKroku = float(input())
    #wspolczynnikKroku = 0.000022
    
    minimumX, kolejneKrokiX = znajdowanieMinimum(punktP,wspolczynnikKroku, funkcjaF, gradientF)
    print("Minimum funkcji f znajduje sie w: ", minimumX)
    
    x = np.arange(-punktP[0],punktP[0],0.5) 
    y = funkcjaF(x)
    
    yKroki = funkcjaF(np.array(kolejneKrokiX,dtype=object))
    
    plt.title("Funkcja f wraz z zobrazowaniem szukania minimum") 
    plt.xlabel("x") 
    plt.ylabel("y") 
    plt.plot(x,y)
    plt.plot(np.array(kolejneKrokiX,dtype=object),yKroki) 
    plt.show()
    

def pojedynczeGzWizualizacja(): #interfejs do jednorazowego znalezienia minimum funkcji g wraz z wizualizacją kolejnych kroków algorytmu
    print("Prosze wprowadzic 2 punkty poczatkowe funkcji g")
    #a= float(input())
    #b= float(input())
    a= 1
    b= 2
    punktP = [a,b]
    
    print("Prosze wprowadzic współczynnik długosci kroku beta")
    #wspolczynnikKroku = float(input())
    wspolczynnikKroku = 0.19
    
    minimumX, kolejneKrokiX = znajdowanieMinimum(punktP,wspolczynnikKroku, funkcjaG, gradientG)
    print("Minimum funkcji g znajduje sie w: ", minimumX)
     
    xa = np.arange(-abs(punktP[0]),abs(punktP[0]),0.5) 
    xb = np.arange(-abs(punktP[1]),abs(punktP[1]),0.5) 
    
    x2 = np.array(np.meshgrid(xa,xb)).T.reshape(-1,2)
    
    
    y2 = [float(funkcjaG(x2[0]))]
    for i in range(1,x2.shape[0]):
        y2.append(funkcjaG(x2[i]))
        
    
    yKroki2 = [float(funkcjaG(np.array(kolejneKrokiX[0])))]
    for i in range(1,len(kolejneKrokiX)):
        yKroki2.append(funkcjaG(np.array(kolejneKrokiX[i])))
    
    plt.title("Funkcja g wraz z zobrazowaniem szukania minimum") 
    plt.plot(x2,y2)
    plt.plot(np.array(kolejneKrokiX),yKroki2) 
    plt.show()
    




#randomParePowtorzenMenuF()
#randomParePowtorzenMenuG()
#pojedynczeFzWizualizacja()
pojedynczeGzWizualizacja()





