# Specyfikacja

API korzysta z mechanizmu autoryzacji OAuth 2.0, którego opis dostępny jest w [RFC-6749](http://tools.ietf.org/html/rfc6749).

# Endpoint do pobierania tokenów

Token dostępowy można uzyskać wykonując request na adres:

    http://application.domain/oauth2/token/

# Ustawienia aplikacji

Aby wygenerować sobie `client_id` i `client_secret` należy w panelu admina (`http://application.domain/admin`) przejść do
zakładki `OAuth2_Provider` -> `Applications` i kliknąć `Dodaj application`. Jako *user* należy wybrać admina, *client type* ustawić na
`public` a w polu *authorization grant type* wybrać `Client credentials`.

