import numpy as np
import pandas as pd

def implementacjaAlgorytmuID3(bazaDanych, cecha, maksymalnaGlebokoscDrzewa): #rozpoczecie algorytmu tworzac pierwszy węzeł drzewa, okreslając szukaną cechę, zbiór danych uczących oraz maksymalną głębokosc drzewa
    bazaDanych_z_naglowkami_kopia = bazaDanych.copy() 
    drzewoT = {} 
    polaCechy = bazaDanych_z_naglowkami_kopia[cecha].unique() 
    tworzenieDrzewa(drzewoT, None, bazaDanych_z_naglowkami, cecha, polaCechy, maksymalnaGlebokoscDrzewa) 
    return drzewoT

def tworzenieDrzewa(bazowyLisc, wartoscPoprzedniegoLiscia, bazaDanych, cechaT, polaCechyT, maksymalnaGlebokoscDrzewa): #tworzenie drzewa lub kolejnych gałęzi drzewa, w zależnosci od tego czy pozostały jeszcze jakies parametry atrybutów członka populacji, oraz czy maksymalna głębokosc drzewa nie została osiągnięta. Kolejne gałęzie drzewa są okreslane tymi samymi krytetriami co liscie (w praktyce liscie są potencjalnymi gałęziami które zmieniają się w nie przy sprzyjających warunkach)
    if bazaDanych.shape[0] != 0 and maksymalnaGlebokoscDrzewa>0: 
        atrybutONajwiekszejIlosciInformacji = cechaZNajmniejszaEntropia(bazaDanych, cechaT, polaCechyT) 
        drzewoT, bazaDanych = tworzenieLisciaDrzewa(atrybutONajwiekszejIlosciInformacji, bazaDanych, cechaT, polaCechyT, maksymalnaGlebokoscDrzewa-1) 
        nastepnyLisc = None
        
        if wartoscPoprzedniegoLiscia != None: 
            bazowyLisc[wartoscPoprzedniegoLiscia] = dict()
            bazowyLisc[wartoscPoprzedniegoLiscia][atrybutONajwiekszejIlosciInformacji] = drzewoT
            nastepnyLisc = bazowyLisc[wartoscPoprzedniegoLiscia][atrybutONajwiekszejIlosciInformacji]
        else: 
            bazowyLisc[atrybutONajwiekszejIlosciInformacji] = drzewoT
            nastepnyLisc = bazowyLisc[atrybutONajwiekszejIlosciInformacji]
        
        for lisc, galaz in list(nastepnyLisc.items()): 
            if galaz == "doRozwinieca": 
                bazaDanych_nowa = bazaDanych[bazaDanych[atrybutONajwiekszejIlosciInformacji] == lisc] 
                tworzenieDrzewa(nastepnyLisc, lisc, bazaDanych_nowa, cechaT, polaCechyT, maksymalnaGlebokoscDrzewa-1) 
   

def tworzenieLisciaDrzewa(atrybut, bazaDanychT, cechaT, polaCechyT, maksymalnaGlebokoscDrzewa): #tworzenie pojedynczego liscia drzewa na podstawie liczenia entropii dla poszczególnych atrybutów członka populacji uczącej. Wybierany atrybut jest wykluczany z kolejnego zbioru drzewa, a wybierany jest na podstawie tego iż, jest on tym atrybutem który najbardziej z wszystkich pozostałych wpływa na badaną cechę, także wybranie tego atrybutu swiadczy że on w następnej kolejnocsci powinien zostac rozpatrzony
    iloscDanegoAtrybutu = bazaDanychT[atrybut].value_counts(sort=False) 
    drzewo = {} 
    
    for wartoscAtrybutu, liczba in iloscDanegoAtrybutu.iteritems():
        bazaDanych_bezCechy = bazaDanychT[bazaDanychT[atrybut] == wartoscAtrybutu] 
        
        czyPrzypisane = False 
        for poleCechy in polaCechyT: 
            licznikCechy = bazaDanych_bezCechy[bazaDanych_bezCechy[cechaT] == poleCechy].shape[0] 

            if licznikCechy == liczba: 
                drzewo[wartoscAtrybutu] = poleCechy 
                bazaDanychT = bazaDanychT[bazaDanychT[atrybut] != wartoscAtrybutu] 
                czyPrzypisane = True
        if czyPrzypisane == False: 
            drzewo[wartoscAtrybutu] = "doRozwinieca" 
            
    return drzewo, bazaDanychT


def entropia(bazaDanychT, cechaT, polaCechyT): #funkcja liczaca entropie dla pojedynczego przypadku parametrów dla konkretnych atrybutów pojedyńczego członka populacji uczącej
    liczbaDanych = bazaDanychT.shape[0] 
    entropiaOgolem = 0
    
    for poleA in polaCechyT: 
        liczbaPolaCechy = bazaDanychT[bazaDanychT[cechaT] == poleA].shape[0] 
        entropiaAtrybutuT = - (liczbaPolaCechy/liczbaDanych)*np.log2(liczbaPolaCechy/liczbaDanych) 
        entropiaOgolem += entropiaAtrybutuT 
    #print(total_entr)
    return entropiaOgolem


def entropiaAtrybutu(bazaDanychT, cechaT, polaCechyT): #funkcja liczy entropie jaka wprowadza poszczegolny atrybut w danej sytuacji drzewa
    liczbaAtrybutow = bazaDanychT.shape[0]
    entropiaOgolem = 0
    
    for poleA in polaCechyT:
        liczbaPolaCechy = bazaDanychT[bazaDanychT[cechaT] == poleA].shape[0]  
        klasaEntropii = 0
        if liczbaPolaCechy > 0:
            klasaEntropii = - (liczbaPolaCechy/liczbaAtrybutow) * np.log2(liczbaPolaCechy/liczbaAtrybutow)  
        entropiaOgolem += klasaEntropii
    return entropiaOgolem


def przyrostWiedzy(atrybut, bazaDanych, cecha, polaCechy): #funkcja obliczajaca przyrost wiedzy zwiazany z danym atrybutem w poszczególnym członku populacji uczącej
    polaAtrybutu = bazaDanych[atrybut].unique() 
    iloscDanych = bazaDanych.shape[0]
    wiedzaAtrybutu = 0.0
    
    for poleA in polaAtrybutu:
        wartoscPola = bazaDanych[bazaDanych[atrybut] == poleA] 
        iloscWartosciPola = wartoscPola.shape[0]
        entropiaAtrybutuT = entropiaAtrybutu(wartoscPola, cecha, polaCechy) 
        wiedzaAtrybutu += (iloscWartosciPola/iloscDanych) * entropiaAtrybutuT
        
    return entropia(bazaDanych, cecha, polaCechy) - wiedzaAtrybutu 


def cechaZNajmniejszaEntropia(bazaDanych, cecha, polaCechy): #funkcja ktora z podanych mozliwych pol atrybutow wybierany jest ten atrybut ktory gwarantuje dla drzewa najmniejsza wartosc entropii, a wiec najwiekszy przyrost wiedzy
    naglowki = bazaDanych.columns.drop(cecha) 
                                            
    maxPrzyrostWiedzy = -1
    maxPrzyrostWiedzy_atrybut = None
    
    for naglowek in naglowki:  
        przyrostWiedzy_atrybutu = przyrostWiedzy(naglowek, bazaDanych, cecha, polaCechy)
        if maxPrzyrostWiedzy < przyrostWiedzy_atrybutu: 
            maxPrzyrostWiedzy = przyrostWiedzy_atrybutu
            maxPrzyrostWiedzy_atrybut = naglowek
            
    return maxPrzyrostWiedzy_atrybut





def wykonaniePrekdykcjiZDrzewa(drzewo, atrybuty): #jest to funkcja przewidujaca wartosc pola 'irradiant' na podstawie wygenerowanego za pomoca algorytmu id3 drzewa stworzonego na bazie zbioru uczacego
    if not isinstance(drzewo, dict):
        return drzewo
    else:
        lisc = next(iter(drzewo))
        wartoscLiscia = atrybuty[lisc]
        if wartoscLiscia in drzewo[lisc]:
            return wykonaniePrekdykcjiZDrzewa(drzewo[lisc][wartoscLiscia], atrybuty)
        else:
            return None



def ocenaDokladnosci(drzewo, bazaDanych, cecha): #jest to funkcja porownujaca predykcje wykonane na podstawie wygenerowanego wczesniej drzewa, do pliku walidacyjnego tychze danych
    licznikPrawidlowychPredykcji = 0
    licznikWadliwychPredykcji = 0
    for i, j in bazaDanych.iterrows():
        tempWynik = wykonaniePrekdykcjiZDrzewa(drzewo, bazaDanych.iloc[i])
        if tempWynik == bazaDanych[cecha].iloc[i]:
            licznikPrawidlowychPredykcji += 1
        else:
            licznikWadliwychPredykcji += 1
            
    return licznikPrawidlowychPredykcji / (licznikPrawidlowychPredykcji + licznikWadliwychPredykcji)



bazaDanych_z_naglowkami = pd.read_csv("breast-cancerLearn.csv") #odczytywana jest baza danych z pliku bazy breast-cancer

maksymalnaGlebokoscDrzewa=8 #narzucana jest maksymalna glebokosc drzewa

drzewo = implementacjaAlgorytmuID3(bazaDanych_z_naglowkami, 'irradiant',maksymalnaGlebokoscDrzewa) #tworzone jest drzewo na podstawie podanych danych

bazaDanych_z_naglowkami_do_weryfikacji = pd.read_csv("breast-cancerVer.csv") #odczytywana jest baza danych z pliku bazy breast-cancer sluzaca do walidacji
bazaDanych_z_naglowkami_do_testow = pd.read_csv("breast-cancerTest.csv") #odczytywana jest baza danych z pliku bazy breast-cancer sluzaca do testow


dokladnosc = ocenaDokladnosci(drzewo, bazaDanych_z_naglowkami_do_testow, 'irradiant')
print("Dokladnosc algorytmu dla max glebokosci drzewa " + str(maksymalnaGlebokoscDrzewa) +" wyniosla: ", dokladnosc) #wyswietlana jest dokladnosc stworzonych predykcji na podstawie zbioru walidacyjnego, sprawdzana z zbiorem testujacym
