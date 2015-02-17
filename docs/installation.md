Aby zainstalować projekt trzeba mieć:

* Python 2.7
* virtualenv
* npm
* bower

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