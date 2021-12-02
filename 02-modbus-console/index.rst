Modbus konzolna aplikacija
==========================

Ovo poglavlje pokriva prvi dio radionice s 4. predavanja, spajanje na Modbus
uredaj preko konzolne aplikacije i ispis ocitane vrijednosti na izlaz. Rjesenje
je objavljeno na `repozitoriju s predavanja
<https://github.com/rppiot2021/02-modbus-console>`_, a ovaj dio opisuje korake
potrebne za dolazak do njega.

Zadatak
-------

Na adresi 161.53.17.239:8502 preko Modbus TCP protokola posluzuju se podatci o
temperaturi s termometra. Specifikacija uredaja je dostupna na `ovoj adresi
<https://download.inveo.com.pl/manual/nano_t_poe/user_manual_en.pdf>`_.
Potrebno je napraviti konzolnu aplikaciju koja ce se spojiti na ovaj uredaj i
ispisivati ocitanja temperature. Nije potrebno pretjerano se zamarati s
trazenjem optimalne arhitekture, jer ce se kasnije razvijati rjesenje bazirano
na tehnologijama iz ``hat-open`` projekta, koje pokrivaju te probleme.

Rjesenje
--------

Kao i prosli put, prvi korak je proucavanje komunikacijskog sucelja uredaja s
kojim radimo. Gledanjem `specifikacije
<https://download.inveo.com.pl/manual/nano_t_poe/user_manual_en.pdf>`_, vidimo
da podatcima o temperaturi mozemo pristupiti na vise nacina, no mi se u sklopu
zadatka fokusiramo na Modbus, cije sucelje je opisano u poglavlju 7.7. U njemu
se nalazi nekoliko tablica na temelju kojih mozemo pristupati podatcima,
konfigurirati uredaj i sl. Tablice imaju stupce `Address`, `Name`, `R/W` i
`Description`. `Address` nam je najzanimljiviji podatak, njega mozemo
intepretirati kao identifikator ocitanja. Po Modbus protokolu, ocitanja se
modeliraju kao sekvencijalna memorija i klijenti koji se spajaju na Modbus
uredaje, pristupaju podatcima tako da salju zahtjeve za citanje odredene
adrese. Sto se tice ostalih stupaca, po `Description` mozemo vidjeti semantiku
svake adrese. Vidimo da adresa 4004 ima informaciju o temperaturi pomnozenu s
10. To je adresa kojoj cemo pristupati preko nase konzolne aplikacije.

Drugi korak je nabavljanje komunikacijskog drivera za Modbus. To opet mozemo
koristiti `hat-drivers <https://hat-drivers.hat-open.com>`_ paket, ovaj put
`Modbus implementaciju
<https://hat-drivers.hat-open.com/py_api/hat/drivers/modbus/index.html>`_.
Vidimo kako ona ima razne funkcije za kreiranje konekcije, na temelju tipa
konekcije koju zelimo otvoriti cemo odabrati jednu od ``create_...`` funkcija.
S obzirom da se uredaj ponasa kao slave (posluzitelj), to znaci da ce se nasa
konzolna aplikacija ponasati kao master (klijent). Dodatno, komuniciramo preko
TCP-a, ne preko serial porta, tako da cemo koristiti funkciju
`hat.drivers.modbus.create_tcp_master
<https://hat-drivers.hat-open.com/py_api/hat/drivers/modbus/index.html#hat.drivers.modbus.create_tcp_master>`_.
Ova funkcija prima dva obvezna argumenta, ``modbus_type`` i ``address``.
``modbus_type`` je tip Modbus uredaja s kojim se radi, to je enumeracija
definirana od strane biblioteke `hat.drivers.modbus.ModbusType
<https://hat-drivers.hat-open.com/py_api/hat/drivers/modbus/common.html#hat.drivers.modbus.common.ModbusType>`_.
Radimo s TCP-om, tako da je ``ModbusType.TCP`` ispravan tip. ``address`` je
struktura podataka koja predstavlja TCP adresu, definirana na
`hat.drivers.tcp.Address
<https://hat-drivers.hat-open.com/py_api/hat/drivers/tcp.html#hat.drivers.tcp.Address>`_.
Tu unosimo IP adresu i port na kojoj termometar posluzuje podatke. Uz sve ovo,
vidimo da je ``create_tcp_master`` funkcija ``async`` te da ju je potrebno
pokretati kroz asyncio infrastrukturu.

Temeljem svega spomenutog, dolazimo do prve verzije rjesenja, gdje se samo
spajamo na termometar:

.. literalinclude:: solutions/1_connect.py
   :language: python

``create_tcp_master`` vraca objekt tipa `hat.drivers.modbus.Master
<https://hat-drivers.hat-open.com/py_api/hat/drivers/modbus/master.html#hat.drivers.modbus.master.Master>`_.
Gledanjem njegove konfiguracije, vidimo da on ima funkciju `read
<https://hat-drivers.hat-open.com/py_api/hat/drivers/modbus/master.html#hat.drivers.modbus.master.Master>`_.
Ona ima obvezne argumente ``device_id``, ``data_type`` i ``start_address``.

``device_id`` oslanja se na cinjenicu da Modbus protokol moze biti realiziran
kao `multidrop <https://en.wikipedia.org/wiki/Multidrop_bus>`_. To znaci da na
jednu konekciju moze biti spojeno vise stvarnih uredaja i argumentima poput
``device_id``-a se specificira kojem uredaju se treba proslijediti taj zahtjev.
U nasem konkretnom slucaju, nemamo vise uredaja u multidropu, pa je
prihvatljiva vrijednost za identifikator 1.

``data_type`` referencira tip podatka koje Modbus moze posluzivati. Protokol
podrzava tipove poput coil i holding register (nazivi iz povjesnih razloga kad
se radilo s fizickim registrima i zavojnicama). Po tablici iz specifikacije
uredaja, vidimo da je temperatura zapisana u holidng register-u, tako da
koristimo enumeraciju ``hat.drivers.modbus.DataType.HOLDING_REGISTER`` kao
``data_type``.

``start_address`` je adresa na kojoj je podatak posluzen. Po tablici u
dokumentaciji to se posluzuje na adresi 4004, tako da je to vrijednost.
Isprobavanjem rjesenja, videno je da je ova informacija zapravo zapisana na
adresi 4003, sto je vjerojatno zbog pocetnog indeksa, dokumentacija krece od 1,
dok Modbus driver pretpostavlja start od 0. Dakle, ``start_address`` je 4003.

Recimo da zelimo kontinuirano slati upite za ocitanjem na uredaj svakih 5
sekundi. Onda bi nam rjesenje izgledalo ovako:

.. literalinclude:: solutions/2_complete.py
   :language: python

Ovime na konzolni ispis dobivamo temperaturu pomnozenu s 10. Rjesenje bi se
dalo raspisivati detaljnije, kao u prvom zadatku, uvoditi konkretnu arhitekturu
i sl., no ovdje je ideja nastaviti s Hat tehnologijama. Iduci zadatak opisuje
kako izvesti istu stvar, koristenjem Hatove infrastrukture.
