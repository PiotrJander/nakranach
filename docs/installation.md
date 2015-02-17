Aby zainstalować projekt trzeba mieć:

* Python 2.7
* virtualenv
* npm
* bower

Jak już to mamy, to tworzymy sobie bazę w MySQL (ustawiając kodowanie na utf-8). Następnie
kopiujemy plik `app/settings/db.py.base` do `app/settings/db.py` i uzupełniamy znajdujące się
w nim dane do połączenia z bazą.

Instalacja składa się z następujących poleceń (wykonywanych w głównym katalogu projektu):

    virtualenv env
    . env/bin/activate
    npm install .
    grunt install
    pip install -r requirements/dist.txt
    ./manage.py syncdb
    ./manage.py migrate

Krok opcjonalny jakby coś nie pojszło:

    Pytać Strusia.

Aby uruchomić serwer developerski to robimy:

    ./manage.py runserver 0.0.0.0:8000