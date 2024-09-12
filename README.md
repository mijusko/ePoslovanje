# Find Movie - Mihajlo Jankovic 616-2019

## Portal za pretragu i preuzimanje filmova - ePoslovanje


U ovom projektnom zadatku je kreirana i opisana struktura aplikacije koja omogucava pretragu i preuzimanje filmova kao i prevoda za iste. Korisnici mogu da pretrazuju filmove i nije im potrebna nikakva prijava za odredjene funkcije(kao sto je gledanje trejlera filmova, citanje informacija o filmovima i njihova pretraga), dok za preuzimanje filmova(scrapping torrent magnet linkova) kao i prevoda tj. titlova(scrapping zipovanih titlova u .srt formatu), kao i cuvanje filmova u Bookmarks, potrebna j prijava. Korisnici mogu da se registruju i prijave na portal i onda im se pruzaju sve mogucnosti na portalu. Pored obicnih korisnika i registrovanih korisnika, na portalu postoji i super korisnik odnosno admin koji ima svoj dashboard na kom moze da prati desavanja vezana za korisnike, njihove tokene sto aktivne sto neaktivne da upravlja njihovim nalozima tako sto moze da ih menja pa cak i ukloni, a takodje moze i da dodaje korisnike.
<br>

Koriscene tehnologije:

- Front end: ANGULAR (HTML, CSS, JavaScript, Bootstrap)
- Back end: Django, SQLite3, TMDB Api
- Unit testovi: Pytest
- Web Scrapping i automatizacija: Selenium, Python
  <br>


```
Admin prijava: 
username - admin
password - admin123
```


## Vrste korisnika:

- Super korisnik(admin)
- Korisnik sa nalogom
- Korisnik bez naloga

<hr style="font-size: 10px;margin: auto;" width="100%" >


## Pokretanje aplikacije

- Kompletna aplikacija se nalazi na repozitorijumu i kada se preuzme potrebno je posedovati ono sto navedena arhitektura aplikacije zahteva. U slucaju da se pokrece preko Visual Studio Code-a dovoljno je otvoriti folder sa aplikacijom i u terminalu pokrenuti virtuelno okruzenje komandom ".\env\Scripts\Activate" nakon toga se pokrece server komandom "python manage.py runserver". Nakon sto se pokrene server pokrece se angular takodje u termnalu komandom "ng serve" i u pretrazivacu je dovoljno uneti "http://localhost:4200", a ako zelite da pristupite glavnom korisniku: "http://127.0.0.1:8000/admin/", nacin prijave je vec naveden iznad. PhpMyAdmin je na: "http://localhost:8082".

<img style="margin-left: 50px;" src="../Screenshots/Docker.png" width="600px">

## Screenshots:

#### Pocetna Strana
<img src="../Screenshots/Pocetna_Strana.png" width="600">

#### Login Strana
<img src="../Screenshots/Login_Strana.png" width="600">

#### Strana za Pretragu
<img src="../Screenshots/Pretraga_Strana.png" width="600">

#### Strana koja prikazuje Vest
<img src="../Screenshots/Vest_Strana.png" width="600">

#### Strana za komentare
<img src="../Screenshots/Komentari_Strana.png" width="600">

#### Urednik Login
<img src="../Screenshots/Urednik_Login.png" width="600">

#### Urednik Pocetna
<img src="../Screenshots/Urednik_Pocetna.png" width="600">

