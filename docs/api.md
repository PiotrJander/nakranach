# Pobranie listy pubów

Aby pobrać listę pubów należy skorzystać z endpointa:

    GET http://application.domain/api/pubs

Dostęp do poszczególnych pubów/kranów realizowany jest przez URLe zwracane przez api.

# Pobranie listy ostatnich zmian

Aby pobrać listę ostatnich zmian ze wszystkich pubów korzysta się z adresu:

    GET http://application.domain/api/changes

Do adresu można dodać opcjonalny parametr `count` który określa maksymalną liczbę zmian do pobrania
(domyślnie jest to 10). Zmiany są posortowane od najpóźniejszej.