# Felhasználói doksi

### Indítás

#### Lokálisan
Adjuk ki a parancsot az elindításhoz:
```shell
$ python manage.py runserver
```
vagy ha több verzió is van a gépen:
```shell
$ py -3 manage.py runserver
```

![](doc/start.png)

#### Heroku-n
Itt nincs semmi dolgunk, ugorhatunk a következő lépésre, hiszen minden verzió a masterről automatikusan deployol a Heroku-s rendszerre.


### Regisztráció / Bejelentkezés

Navigáljuk a http://127.0.0.1:8000-es oldalra vagy a https://instafollowo.herokuapp.com oldalra.

Ha nem vagyunk bejelentkezve, akkor automatikusan a login felületre dob minket az oldal. Itt kattintsunk a Sign up linkre, vagy jelentkezzünk be,
ha már van felhasználónk.
#### Login
![](doc/login.png)

#### Signup felület
![](doc/signup.png)

#### Kitöltött verzió
![](doc/signup_filled.png)

Majd értelemszerűen kattintsunk a Sign up-ra.

### Dashboard

Bejelentkezés után a dashboard felületre érkezünk, ahol meg tudjuk nézni, hogy hány regisztrált felhasználó van
az oldalon és összesen hány Instagram account van már rögzítve. Terveztük a naponkénti follower számot követni, viszont
erre nincs hivatalos API és úgy gondoltuk, hogy az már túl sok munka lenne, ha ezt is implementálnánk, így a grafikon
csak placeholderként ottmaradt, hogy ne legyen annyira üres :)

![](doc/dashboard.png)

### Instagram accountok

![](doc/empty_account_page.png)

Az accounts fülre kattintva meg tudjuk tekinteni a már felvett Instgram felhasználóinkat. Egy friss regisztrációval ez nyilván üres.
Az add new account gombra kattintva tudunk újat felvenni.

![](doc/new_account.png)

Az új felhasználó hozzáadása után a kis háromszögre kattintva elindíthatjuk a botot a kívánt accounton.

![](doc/started.png)

Jelenleg úgy van beállítva a rendszer, hogy 5 percenként followol egy accountot a megadott kritériumok szerint.
Ennek nyoma csak a konzolban van, valamint ha bejelentkezünk az Instagram accountunkba az oldalon.

![](doc/followed.png)


### A munka gyümölcse

Meglett az első kettő followerünk, akik a bot miatt followoltak vissza :)

![](doc/success.png)
