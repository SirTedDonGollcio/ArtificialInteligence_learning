%%
clear all
close all

%Wczytanie danych do uczenia sieci oraz danych do testowanai sieci

[dane,~,~] = xlsread('C:\Users\pludy\OneDrive\Pulpit\SNB\nauka');
[dane_testowe,~,~] = xlsread('C:\Users\pludy\OneDrive\Pulpit\SNB\test');

%%
%Ustawienie parametrow sieci na podstawie danych, ktore zostaly wczytane

oczekiwane_wyjscie = dane(:,1);
wejscia = dane(:,2:width(dane));
ilosc_wektorow_wejsciowych = length(dane);
ilosc_parametrow = width(dane)-1;
ilosc_neuronow_w_warstwie_ukrytej = round(sqrt(ilosc_parametrow+1));

%Ustawienie parametrów przez użytkownika
iteracje = 1e7; 
eta = 1e-4;     %parametr eta algorytmu uczenia
warunek = 0.04;    %blad sieci, ktory zatryzmuje procs uczenia
co_ile_rysowac = 10000; %co ile iteracji rysowac blad na wykresie
granica_ufnosci_d = 0.4; %wartości na wyjściu poniżej tego parametru będa uznawane za 0
granica_ufnosci_g = 0.7; %%wartości na wyjściu powyżej tego parametru będa uznawane za 1


% wektory wag ustawiane na losowe wartosci
wagi1 = 0.005*rand(ilosc_neuronow_w_warstwie_ukrytej,ilosc_parametrow);
wagi2 = 0.005*rand(1,ilosc_neuronow_w_warstwie_ukrytej);

% deklaracja pustych wektorow do wykresu i wartosci bledu
wykres = zeros(1,iteracje);
blad_calkowity= (ones(1,ilosc_wektorow_wejsciowych))/ilosc_wektorow_wejsciowych;
i=1;
blad_uczenia = 1;

%petla uczaca siec
while (blad_uczenia >= warunek)
    % wylosowanie numeru wektora wejsciowego
    k=(randi(ilosc_wektorow_wejsciowych,1,1));
    pierwszy_wektor_uczacy = wejscia(k,:);
    
    %obliczenie wejscia i wyjscia neuronow ukrytych
    pobudzenie_neuronow_ukrytych = pierwszy_wektor_uczacy*wagi1';
    wyjscie_neuronow_ukrytych = FunkcjaAktywacji(pobudzenie_neuronow_ukrytych);
    
    %obliczenie wejscia i wyjscia neuronu wyjsciowego
    pobudzenie_neuronu_wyjsciowego = wyjscie_neuronow_ukrytych*wagi2';
    stan_neuronu_wyjsciowego = FunkcjaAktywacji(pobudzenie_neuronu_wyjsciowego);

    %obliczenie błędów neuronów ukrytych i wejsciowych
    blad_wyjscia = (oczekiwane_wyjscie(k)-stan_neuronu_wyjsciowego) * PochodnaFunkcjiAktywacji(pobudzenie_neuronu_wyjsciowego);
    blad_warstwy_ukrytej = PochodnaFunkcjiAktywacji(pobudzenie_neuronow_ukrytych) * sum(wagi2.*blad_wyjscia);  

    %modyfikacja wartosci wag na podstawie wyliczonych bledow
    wagi2 = wagi2 + eta * blad_wyjscia * wyjscie_neuronow_ukrytych;
    wagi1 = wagi1 + eta * (blad_warstwy_ukrytej' * pierwszy_wektor_uczacy);
    
    %wyliczenie błędu w danej iteracji
    blad_calkowity(k) = (0.5*(oczekiwane_wyjscie(k) - stan_neuronu_wyjsciowego)^2)/ilosc_wektorow_wejsciowych;    
    blad_uczenia = sum(blad_calkowity(:));
    wykres(i) = blad_uczenia;
    
    %narysowanie wartosci bledu na wykresie 
    if (mod(i,co_ile_rysowac)==0)
        figure(1)
        plot(i,wykres(i),'-o')
        hold on
    end
    i=i+1;
end

%% Testowanie sieci neuronowej

%przekazanie wartosci wag z nauczonej sieci do testowania
wagi_testowe_1 = wagi1;
wagi_testowe_2 = wagi2;

%dostosowanie parametrow sieci do danych testujacych
oczekiwane_wyjscie_test = dane_testowe(:,1);
wejscia_test = dane_testowe(:,2:width(dane_testowe));
ilosc_testow = length(dane_testowe);


%przetestowanie sieci dla wszystkich wektorow testujacych
for j=1:ilosc_testow
    pobudzenie_neuronow_ukrytych_test = wejscia_test(j,:)*wagi_testowe_1';
    wyjscie_neuronow_ukrytych_test = FunkcjaAktywacji(pobudzenie_neuronow_ukrytych_test);
    
    pobudzenie_neuronu_wyjsciowego_test = wyjscie_neuronow_ukrytych_test*wagi_testowe_2';
    stan_neuronu_wyjsciowego_test(j) = FunkcjaAktywacji(pobudzenie_neuronu_wyjsciowego_test); 
    
    blad_calkowity_test(j) = (0.5*(oczekiwane_wyjscie_test(j) - stan_neuronu_wyjsciowego_test(j))^2)/ilosc_testow;        
end

blad_testowania = sum(blad_calkowity_test(:));

%tablica opisujaca wyjscia sieci
odpowiedzi = (SortujOdpowiedzi(stan_neuronu_wyjsciowego_test,granica_ufnosci_d,granica_ufnosci_g))';

%tablica przechowujaca oczekiwane wyjscia sieci
klucz_odpowiedzi = oczekiwane_wyjscie_test;
prawdziwie_negatywne = 0;
prawdziwie_pozytywne=0;
falszywie_negatywne = 0;
falszywie_pozytywne=0;

%wyliczenie parametrów opisujacych jakos sieci
for i = 1:ilosc_testow
    if (odpowiedzi(i) ==0 && klucz_odpowiedzi(i) == 0)
        prawdziwie_negatywne = prawdziwie_negatywne +1;
    elseif (odpowiedzi(i) ==1 && klucz_odpowiedzi(i) == 1)
        prawdziwie_pozytywne = prawdziwie_pozytywne+1;
    elseif (odpowiedzi(i) ==1 && klucz_odpowiedzi(i) == 0)
        falszywie_pozytywne = falszywie_pozytywne+1;
    elseif (odpowiedzi(i) ==0 && klucz_odpowiedzi(i) == 1)
        falszywie_negatywne = falszywie_negatywne+1;
    end
end    


czulosc = (prawdziwie_pozytywne)/(prawdziwie_pozytywne+falszywie_negatywne)*100
swoistosc = (falszywie_pozytywne)/(falszywie_pozytywne+prawdziwie_negatywne)*100

wyniki = [prawdziwie_pozytywne;prawdziwie_negatywne;falszywie_pozytywne;falszywie_negatywne];

tabela = table(categorical({'prawdziwie_pozytywne';'prawdziwie_negatywne';'falszywie_pozytywne';'falszywie_negatywne'}),wyniki)


%%
function [pobudzenie] = FunkcjaAktywacji(x)
    pobudzenie = tanh(x);
    %pobudzenie = 1./(1+exp(-x));
end

function [wynik] = PochodnaFunkcjiAktywacji(x)
    wynik = 1 - tanh(x).^2;
    %wynik = exp(-x)/(exp(-x) + 1).^2;
end

function [pobudzenie] = FunkcjaAktywacjiSigmoidalna(x)
    pobudzenie = 1./(1+exp(-x));
end

function [posortowane] = SortujOdpowiedzi(odpowiedzi,granicad, granicag)
    posortowane = odpowiedzi;
    posortowane(odpowiedzi>=granicag) = 1;
    posortowane(odpowiedzi<=granicad) = 0;
    %%posortowane(odpowiedzi>granicad && odpowiedzi<granicag) = 0.5;
end