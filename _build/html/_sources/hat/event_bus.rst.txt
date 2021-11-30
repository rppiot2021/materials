hat-event (event bus)
=====================

Prva komponenta koju gledamo je event server. Ona zapravo ima dvostranu ulogu,
prva je da se ponasa kao sabirnica dogadaja, a druga da sadrzi specijalizirane
module za poslovnu logiku. U ovom dijelu fokusiramo se na prvi aspekt,
komunikacijsku sabirnicu. Trenutno cemo napraviti malu digresiju od primjera s
termometrom, da pokazemo neke generalne ideje oko rada s event serverom, koje
su primjenjive u cijelom sustavu.

Event server se pokrece pozivom naredbe ``hat-event``. Ta naredba prima
komandnolinijski argument ``--conf`` kojim joj se predaje putanja do
konfiguracijske datoteke. Ta datoteka je u JSON ili YAML formatu i ima
strukturu propisanu `JSON shemom
<https://github.com/hat-open/hat-event/blob/master/schemas_json/main.yaml>`_.
Minimalna konfiguracija mogla bi biti:

.. literalinclude:: example_event/conf.yaml
   :language: yaml

Pozivom ``hat-event --conf conf.yaml`` (ako je minimalna konfiguracija zapisana
u datoteci ``conf.yaml``) trebao bi se pokrenuti program bez ikakvog ispisa
koji ne zavrsava. Ovaj poziv pokrece sabirnicu dogadaja koja ceka da se na nju
spoje aktori event-driven sustava (proizvodaci i potrosaci dogdaja). Iduci
korak je implementacija aktora. Spajanje na event server radi se preko
`hat.event.client
<https://hat-event.hat-open.com/py_api/hat/event/client.html>`_ modula. Taj
modul u sebi sadrzi implementaciju funkcija za spajanje na event server,
primanje i registraciju dogadaja. Funkcija ``connect`` obavlja spajanje na
server i vraca nazad instancu klase `hat.event.client.Client
<https://hat-event.hat-open.com/py_api/hat/event/client.html#hat.event.client.Client>`_.
Pozivanjem metoda ``receive`` i ``register`` se primaju ili registriraju
dogadaji.

Dogadaji su uredene trojke koje sadrze atribute ``event_type``, ``payload`` i
``source_timestamp``, a konkretna struktura koja se koristi ovisi o tome koja
metoda se pokusava zvati (npr. metoda ``receive`` vraca `hat.event.common.Event
<https://hat-event.hat-open.com/py_api/hat/event/common/data.html#hat.event.common.data.Event>`_,
dok se metodi ``register`` predaje `hat.event.common.RegisterEvent
<https://hat-event.hat-open.com/py_api/hat/event/common/data.html#hat.event.common.data.RegisterEvent>`_,
ali obje imaju parametre ``event_type``, ``payload`` i ``source_timestamp``,
razlika je u tome da ``hat.event.common.Event`` ima neke dodatne parametre koje
mu dodijeli server). ``event_type`` tuple stringova koja sadrzi semanticko
znacenje promjene koja se desila. Po ranije primjeru, ``event_type`` za dogadaj
koji signalizira promjenu ocitanja mjerenja mogao bi biti ``['thermometer1',
'measurement_change']``.  ``payload`` sadrzi podatke specificne za promjenu
koja se desila, npr. za primjer promjene mjerenja, on bi mogao biti broj koji
ozacava novoizmjerenu temperaturu. ``source_timestamp`` je opcionalna vremenska
oznaka u kojoj kreator dogadaja tom dogadaju moze pridruziti oznaku vremena
(npr. kad je izmjerena temperatura). Kako je ``source_timestamp`` opcionalan, u
svim primjerima cemo ga stavljati u ``None``.

Kreator dogadaja
----------------

S ovime na umu, mozemo implementirati prvu skriptu koja ce se ponasti kao
kreator dogadaja. Ona se pokrece, spaja na event server i registrira dogadaj
koji signalizira promjenu nekog arbitrarnog mjerenja. Funkcijom ``connect``
spojiti cemo se na event server. U konfiguraciji servera, pod
``communication/address`` vidimo adresu i port na kojoj server slusa. Tu adresu
predajemo prvom argumentu ``connect`` funkcije. Drugi argument,
``subscriptions`` zasad cemo ostaviti kao praznu listu, a objasnit cemo ga kad
cemo implementirati konzumenta dogadaja za ovaj primjer.

Nakon toga, u beskonacnoj petlji, svake tri sekunde registriramo event ciji je
``event_type`` ``('measurement1', 'change', 'abc')``, ``source_timestamp`` je
``None``, a ``payload`` je JSON-serijalizabilna struktura podataka s jednim
atributom, ``value``, cija vrijednost je nasumicni broj od 0 do 10. To nas
ostavlja s ovakvom konkretnom implementacijom:

.. literalinclude:: example_event/producer.py
   :language: python

Ovaj program ce se upaliti i raditi dok ga se ne ugasi, bez ispisivanja icega,
ali mozete dodati ispise nasumicnih brojeva koji se registriraju. Takoder,
umjesto ``register``, postoji metoda `register_with_response
<https://hat-event.hat-open.com/py_api/hat/event/client.html#hat.event.client.Client.register_with_response>`_
koja vrati nazad instance dogadaja koji su se registrirali, zanimljivo bi bilo
vidjeti njihov ispis.

Konzument dogadaja
------------------

Mogucnost registracije dogadaja nam nema puno koristi ako se ti dogadaji ne
propagiraju do nekih drugih klijenata. Zbog toga imamo potrebu razviti novog
aktora koji bi primao dogadaje koje registrira kreator iz proslog dijela, i
ispisivao ih na konzolu. U proslom dijelu smo kod ``connect`` funkcije
ignorirali argument ``subscriptions`` jer nam tad nije bio potreban, sad cemo
ga koristiti da novostvorenog klijenta "pretplatimo" na dogadaje s odredenom
semantikom. Semantiku dogadaja odreduje njegov ``event_type``, koji je izveden
kao tuple stringova. Ako pogledamo potpis `connect
<https://hat-event.hat-open.com/py_api/hat/event/client.html#hat.event.client.connect>`_
funkcije, vidimo da je pretplata definirana kao lista tuplova stringova,
odnosno novostvoreni klijent se pretplacuje na n tipova dogadaja.

Nakon stvaranja konekcije s pretplatom, iduca metoda klijenta koja nas zanima
je `receive
<https://hat-event.hat-open.com/py_api/hat/event/client.html#hat.event.client.Client.receive>`_.
Kad event server primi dogadaj s tipom koji na koji je klijent pretplacen, on
mu ga posalje. ``receive`` metoda ceka da klijent primi dogadaj i vrati ga na
izlaz.

Na temelju ovoga, mozemo implementirati naseg konzumenta:

.. literalinclude:: example_event/consumer.py
   :language: python

Pokrenemo li konzumenta i kreatora istovremeno, vidjet cemo da konzument
ispisuje dogadaje koje kreator registrira. Pokrenemo li vise kreatora i
konzumenata istovremeno, svaki konzument ce ispisivati dogdaje koje
registriraju svi kreatori.

Dodatno, kod implementacije konzumenta, pretplatili smo ga na dogadaje s tipom
``('measurement1', 'change', 'abc')``, ali implementacija klijenta nam
omogucuje i koristenje `wildcard` elemenata ``'*'`` i ``'?'``. ``?`` moze biti
na bilo kojem mjestu unutar pretplate i daje do znanja event serveru da nam je
svejedno sto se nalazi u tipu dogadaja na tom mjestu. Tako bi legitimna
pretplata bila ``('measurement', '?', 'abc')`` i konzument bi funkcionirao
jednako. Razlika je da, ako bismo imali aktora koji registrira dogadaje s tipom
``('measurement', 'xyz', 'abc')``, i ti dogadaji bi se ispisivali. Wildcard
``'*'`` moze biti samo na kraju pretplate i daje do znanja event serveru da nam
je svejedno sto se nalazi u tipu dogadaja od mjesta gdje je znak postavljen.
Tako bi pretplata ``('measurement', '*')`` pokrivala ``('measurement',
'change', 'abc')`` dogadaje, ali i ``('measurement')``, ``('measurement',
'xyz')``, ``('measurement', '123', '456')``...

Upiti u stare dogadaje
----------------------

Ovaj aspekt event servera nam mozda nece biti potreban u prakticnim zadatcima,
no svejedno ga navodimo radi kompletnosti. Klijenti event servera imaju jos
jednu metodu koju nismo pokrili, `query
<https://hat-event.hat-open.com/py_api/hat/event/client.html#hat.event.client.Client.query>`_.
Vidimo po potpisu funkcije da ona predaje argument tipa `QueryData
<https://hat-event.hat-open.com/py_api/hat/event/common/data.html#hat.event.common.data.QueryData>`_.
Gledanjem dokumentacije te strukture, vidimo da ona ima puno opcionalnih
argumenata koji izgledaju kao filteri. Kad nad klijentom pozovemo ``query``,
event server primi filtere i na temelju njih napravi upit u bazu podataka kojim
pristupi starim dogadajima koji su se registrirali. Onda vrati te dogadaje i
klijent ih izbaci kao rezultat poziva metode ``query``.

`QueryData
<https://hat-event.hat-open.com/py_api/hat/event/common/data.html#hat.event.common.data.QueryData>`_
ima razne argumente:

  * ``event_ids`` filtrira samo one dogadaje s identifikatorima koji su zadani
  * ``event_types`` filtrira dogadaje na temelju njihovog tipa (takoder moze
    imati wildcardove)
  * ``t_from``, ``t_to`` odreduju pocetak i kraj vremenskog intervala
    ``timestamp`` parametra dogadaja (serverova vremenska oznaka)
  * ``source_t_from``, ``source_t_to`` odreduju pocetak i kraj vremenskog
    intervala ``source_timestamp`` parametra dogadaja (klijentova vremenska
    oznaka)
  * ``payload`` filtrira na temelju ``payload`` parametra dogadaja, gleda se
    jednakost
  * ``order_by`` odreduje kako ce vraceni dogadaji biti soritrani
  * ``unique_type`` daje do znanja event serveru da u rezultatu upita ne vrati
    vise dogadaja s istim tipom
  * ``max_results`` je cvrsto ogranicenje na maksimalni broj dogdaja koji su
    vraceni

Mozemo i isprobati ovu funkcionalnost, dosadasnja konfiguracija koristi
implementaciju baze koja ne radi nista, tako da ju je potrebno malo
prilagoditi:

.. literalinclude:: example_event/conf_db.yaml
   :language: yaml

Nakon toga, mozemo pokrenuti kreatora dogadaja, da nam registrira
``('measurement', 'change', 'abc')`` dogadaje. Paralelno mozemo pokrenuti
sljedecu skriptu koja radi upit na bazu:

.. literalinclude:: example_event/query.py
   :language: python

Na konzoli bi se trebali ispisati svi dogadaji koje je kreator registrirao u
proslosti.

Ovime smo pokrili osnove rada s event serverom koji je zajednicki kod svih
komponenti, a u nastavku cemo vidjeti kako Hat komponente i njihovi
specijalizirani moduli koriste tu infrastrukturu da medusobno suraduju i
implementiraju funkcionalnost industrijskih IoT sustava.
