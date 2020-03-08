# IPK projekt1 - HTTP resolver doménových jmen

#### Specifikace
Cílem projektu je implementace severu, který bude komunikovat protokolem HTTP a bude zajišťovat překlad doménových jmen.

#### Vypracovanie
Vypracovanie používa knižnicu `socket` pre pracovanie zo systémovými socketmi. Socket zostáva otvorený až do ukončenia programu. (napr. `ctrl+c`)  
HTTP resolver je napísaný v jazyku **python3**. Spustenie na porte 64000:
```
python3 server.py 64000
```
alebo cez makefile:
```
make run PORT=64000
```

Resolver dokáže spracovat dva operácie: GET a POST.

##### GET

Je implementovaná operácia `resolve`, ktorá dostane adresu a prekonvertuje ju podľa požadovaného typu.
Povolené typy: A, PTR  
  * A: konvertuje z doménového mena a ip adresu
  * PTR: konvertuje z ip adresy na doménové meno

##### POST

Je implementovaná operácia `dns-query`, ktorá dosane zoznam adries ktoré budú prekonvertované podľa požiadavky. Typy sú totožné s typmi v GET.

#### Chybové hlásenia
  * Vstupní URL není správné, je jiné než /resolve či /dns-query - vrací 400 Bad Request.
  * Vstupní parametry pro GET jsou nesprávné nebo chybí - vrací 400 Bad Request.
  * Formát vstupu pro POST není správný - vrací 400 Bad Request.
  * Operace není podporována - je použita jiná operace než GET a POST - vrací 405 Method Not Allowed.
