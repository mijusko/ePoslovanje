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

- Kompletna aplikacija se nalazi na repozitorijumu i kada se preuzme potrebno je posedovati ono sto navedena arhitektura aplikacije zahteva. U slucaju da se pokrece preko Visual Studio Code-a dovoljno je otvoriti folder sa aplikacijom i u terminalu pokrenuti virtuelno okruzenje komandom ".\env\Scripts\Activate" nakon toga se pokrece server komandom "python manage.py runserver". Nakon sto se pokrene server pokrece se angular takodje u termnalu komandom "ng serve" i u pretrazivacu je dovoljno uneti "http://localhost:4200", a ako zelite da pristupite glavnom korisniku: "http://127.0.0.1:8000/admin/", nacin prijave je vec naveden iznad. 


## Screenshots:

#### Pocetna Strana
<img src="/Screenshots/Homepage.png" width="600">

#### Strana za Pretragu
<img src="/Screenshots/Searchpage.png" width="600">

#### Login Strana
<img src="/Screenshots/Login.png" width="600">

#### REgister Strana
<img src="/Screenshots/Register.png" width="600">

#### Podesavanja naloga
<img src="/Screenshots/Settings.png" width="600">

#### Sacuvani filmovi
<img src="/Screenshots/Bookmarks.png" width="600">

#### Film Detalji
<img src="/Screenshots/Movie.png" width="600">

#### Trailer modal
<img src="/Screenshots/Trailer.png" width="600">

#### Torrents
<img src="/Screenshots/Torrents.png" width="600">

#### Subtitles
<img src="/Screenshots/Subtitles.png" width="600">

#### Admin login
<img src="/Screenshots/AdminLogin.png" width="600">

#### Admin DAshboard
<img src="/Screenshots/Dashboard.png" width="600">

#### Admin upravljanje
<img src="/Screenshots/User.png" width="600">