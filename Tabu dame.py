import random
import numpy as np

def ispisi(konfiguracija):
    n = len(konfiguracija)
    n_len = len(str(n))
    hline = ' ' + ' '*n_len + '+---'*n + '+'
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    print(' ', end='')
    for i in range(n):
        print('   ' + letters[i], end='')
    print()

    for i in range(n):
        print(hline)
        print(str(n-i) + ' '*(n_len-len(str(n-i))) + ' ', end='')
        for j in range(n):
            if konfiguracija[j][1] == i + 1:
                 print('| D ', end='')
            else:
                print('|   ', end='')
        print('|')
    print(hline)


# Za prosledjenu konfiguraciju, racuna broj prekrsaja. Dve dame koje se napadaju
# cine jedan prekrsaj. Takodje, ako se dve dame napadaju "preko" trece dame,
# to se takodje ubraja u prekrsaj, jer bi se uklanjanjem srednje dame one
# napadale. Ne moramo proveravati prekrsaje po vertikalama, jer znamo da je
# na svakoj vertikali tacno jedna dama.
def izracunaj_broj_prekrsaja(konfiguracija):
    n = len(konfiguracija)
    brojac = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Ako se dve dame nalaze na istoj horizontali, to je prekrsaj.
            if konfiguracija[i][1] == konfiguracija[j][1]:
                 brojac += 1
            # Provera dijagonala paralelnih glavnoj dijagonali.
            if konfiguracija[i][1] - (i+1) == konfiguracija[j][1] - (j+1):
                brojac += 1
            # Provera dijagonala paralelnih sporednoj dijagonali.
            if konfiguracija[i][1] + (i+1) == konfiguracija[j][1] + (j+1):
                brojac += 1
    return brojac

# Za prosledjeni broj dama, vraca listu parova (dama, pozicija), tako
# da je na svakoj vertikali table tacno jedna dama.
def generisi_pocetnu_konfiguraciju(broj_dama):
    konfiguracija = []
    for i in range(1, broj_dama + 1):
        par = (i, random.randint(1, broj_dama))
        konfiguracija.append(par)
    return konfiguracija

# Na osnovu prosledjene konfiguracije i tabu liste, generise se izmenjena
# okolina, koja je skupovna razlika okoline i tabu liste.
def generisi_okolinu(konfiguracija, tabu_lista):
    okolina = []
    n = len(konfiguracija)
    for i in range(n):
        okolina.extend([(i+1,polje) for polje in range(1,n+1) if konfiguracija[i][1] != polje])
    izmenjena_okolina = list(set(okolina) - set(tabu_lista))
    return izmenjena_okolina

def selektuj_najbolji_potez(okolina, konfiguracija):
    najbolji_potez = okolina[0]
    nova_konfiguracija = [(d, p) if d!=okolina[0][0] else okolina[0] for (d, p) in konfiguracija]
    min_prekrsaja = izracunaj_broj_prekrsaja(nova_konfiguracija)
    for i in range(1, len(okolina)):
        trenutni_potez = okolina[i]
        nova_konfiguracija = [(d, p) if d!=trenutni_potez[0] else trenutni_potez for (d, p) in konfiguracija]
        br_prekrsaja = izracunaj_broj_prekrsaja(nova_konfiguracija)
        if br_prekrsaja < min_prekrsaja:
            najbolji_potez = trenutni_potez
            min_prekrsaja = br_prekrsaja

    return najbolji_potez

# Vrsi tabu pretragu nad konfiguracijama.
def TabuDame(pocetna_konfiguracija, max_iteracija, velicina_tabu_liste):
    trenutna_konf = pocetna_konfiguracija
    ispisi(trenutna_konf)
    najbolja_konf = pocetna_konfiguracija
    n = len(pocetna_konfiguracija)
    brojac = 0

    tabu_lista = []

    while brojac < max_iteracija and izracunaj_broj_prekrsaja(trenutna_konf) > 0:
        izmenjena_okolina = generisi_okolinu(trenutna_konf, tabu_lista)
        if len(izmenjena_okolina) > 0:
            potez = selektuj_najbolji_potez(izmenjena_okolina, trenutna_konf)
            #tabu_lista.extend([(d,p) for (d,p) in trenutna_konf if (d,p)==potez[0]])
            tabu_lista.append(potez)
            trenutna_konf = [(d, p) if d!=potez[0] else potez for (d, p) in trenutna_konf]
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
            ispisi(trenutna_konf)

        if izracunaj_broj_prekrsaja(trenutna_konf) < izracunaj_broj_prekrsaja(najbolja_konf):
            najbolja_konf = trenutna_konf

        if len(tabu_lista) > velicina_tabu_liste:
            tabu_lista.pop(0)

        brojac += 1

    return najbolja_konf




import itertools

def nadji_lokalne_minimume(n):
    lok_min = []

    kombinacije = []
    combos = list(itertools.product(range(1, n+1), repeat=n))
    for comb in combos:
        konfiguracija = []
        for i,num in zip(range(1, n + 1), comb):
            konfiguracija.append( (i, num) )
        kombinacije.append(konfiguracija)

    for konfiguracija in kombinacije:
        okolina = generisi_okolinu(konfiguracija, [])
        potez = selektuj_najbolji_potez(okolina, konfiguracija)
        trenutna_konf = konfiguracija
        trenutna_konf = [(d, p) if d != potez[0] else potez for (d, p) in trenutna_konf]
        if izracunaj_broj_prekrsaja(trenutna_konf) == izracunaj_broj_prekrsaja(konfiguracija):
            lok_min.append(konfiguracija)

    return lok_min

import os

n = 5

prime = n * n
prime_konfiguracija = []

lok_min = nadji_lokalne_minimume(n)

konfiguracija = random.choice(lok_min)

konfiguracija = generisi_pocetnu_konfiguraciju(15)

for i in range(100):
    nova_konfiguracija = TabuDame(konfiguracija, 100, 20)

    if (izracunaj_broj_prekrsaja(nova_konfiguracija) < prime):
        prime = izracunaj_broj_prekrsaja(nova_konfiguracija)
        prime_konfiguracija = nova_konfiguracija

        if prime == 0:
            break