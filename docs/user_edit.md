left:

    >> Profil podsumowanie

    avatar | create gravatar prompt

    fullname

    email

    roles

right - only one tab:

    fname, lname

    email

    password x2


To consider:

1. only the user can edit his profile -> restrict access
2. url: /user/emailhash

a pub admin can invite a user to work in the pub by email


Gravatar:

Scenario 1:
user creates his account
she types her email
we could check her gravatar now
and load a gravatar if she has one, or provide her a link to gravatar.com
avatar is not required

avatar url redundant
just use email
but we could prompt the user to create an avatar if she doesn't have one yet

we could also hardcode url -- size is given by http get param anyway
this way we use avatar_url field and don't use 3rd plib
do this

1. upon account creation, don't ask for avatar
2. then try to retrieve avatar, else prompt to create one

but first read about dj form validation
you can't read all Dj docs - and it's deadly boring

read the docs when you really need
now I need to read forms docs


Concerning forms:
1. admins can add/edit/delete users
2. non-admins can edit their own profiles

url:
user/add
user/update/emailhash
user/delete/emailhash

NOTE: the edit view combines detail and delete func
NOTE: there's also the generic FormView

1. Add
a) add an account through registration
b) add an account by admin
BUT: association with pubs

a user can have more than one role and work in more than one pub - we want to manage that from
one place

but then two different admins could update user's profile

we don't want an admin to modify user's name, email, or password
so let's not give him full control

someone could gain access to admin account and break many user profiles

you can only create an account for yourself, and admin can't update your fields

you can only have one role in one pub, and you can be associated with a pub only through one
relation

how pubs and users become associated?

user can request to be associated with a pub; a list of all pubs in the system is publicly available
multiple choice

admin of pub P can invite users by typing email, email must be validated for presence in the system
user can accept or reject invitation

invitation may contain the role

once pub P and user U are associated, pub admin can change U's role

both parties can leave the association at any point

Zapytać Matiego:
1. can admin create a new user and associate him with a pub?
against: many pubs, email validation, identity theft

2. how do users and pubs associate?
- user requesting; public list of pubs
- admin requesting

3. voluntary withdrawal from association
- I'm a bartender at P; can I leave at any moment?