1. No interface for adding pubs. Pubs are only added by Makimo, as is the first admin.
1a. Many admins in a pub permitted. An admin can't change his own role, but can change
    the role of other admins.
2. Registration. Each user needs an app, so registration only in an app. ???
3. Invitation. A user email must already be registered in the system before he can be invited.

how invitation goes:
admin enters a user email, one at a time; submits
if email in the system, user/list
if not, redisplay form, message

form: if admin in more than one pub, choose the pub to invite
always display choose pub field
but

do I need django crispy forms? not now; try to play with HTML for forms
would be nice to have a horizontal form
but first of all create two columns
in the right column list existing users: pub/role/name:email

we could alternatively have a list of managed pubs, and link: "Zaproś do pubu X"

albo i to, i to

jeżeli admin zarządza jednym pubem, pole Wybierz pub nieaktywne

na początek html: prawa columna