# IPK projekt1 - HTTP resolver doménových jmen

#### Specifikace
Cílem projektu je implementace severu, který bude komunikovat protokolem HTTP a bude zajišťovat překlad doménových jmen.

#### Vypracovanie
HTTP resolver je napísaný v jazyku **python3**. Vypracovanie používa knižnicu `socket` pre pracovanie zo systémovými socketmi. Socket zostáva otvorený až do ukončenia programu. (napr. `ctrl+c`)  
Príkladové spustenie na porte 64000:
```
python3 server.py 64000
```
alebo cez makefile:
```
make run PORT=64000
```

Resolver dokáže spracovat dve operácie: GET a POST.

##### GET

Je implementovaná operácia `resolve`, ktorá prekladá danú adresu na požadovaný typ.  
Povolené typy:  
  * **A** prekladá doménové meno na ip adresu
  * **PTR** prekladá ip adresu na doménové meno

##### POST

Je implementovaná operácia `dns-query`, ktorá prekladá zoznam adries na typ podľa požiadavky. Typy sú totožné s typmi v GET.

#### Chybové hlásenia
  * Vstupní URL není správné, je jiné než /resolve či /dns-query - vrací 400 Bad Request.
  * Vstupní parametry pro GET jsou nesprávné nebo chybí - vrací 400 Bad Request.
  * Formát vstupu pro POST není správný - vrací 400 Bad Request.
  * Operace není podporována - je použita jiná operace než GET a POST - vrací 405 Method Not Allowed.
