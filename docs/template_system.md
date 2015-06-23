Szablony są zorganizowane trzypoziomowo:

1. base.html
    - zawiera head strony
    - cztery bloki: styles, lanceng_body_classes, body, scripts
    - block lanceng_body_classes został wyodrębniony, bo chociaż większość widoków
        lancenga wymaga jedynie klasy tooltips na body, to niektóre widoki wymagają
        dodatkowych klas
    - szablon base.html został wyodrębniony na potrzeby widoku logowania, który
        nie powinien wyświetlać panelu bocznego i paska górnego

2. base_framed.html
    - z tego szablony powinno dziedziczyć większość widoków lancenga
    - poszerza base.html o panel boczny i pasek górny
    - wprowadza blok content, do którego ma trafiać główna zawartość strony
    - każdy szablon dziedziczący z base_framed.html wymaga obiektu Profile, który
        reprezentuje zalogowanego użytkownika

3. *.html - szablony powinny dziedziczyć z base_framed.html
