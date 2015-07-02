1. No interface for adding pubs. Pubs are only added by Makimo, as is the first admin.
1a. Many admins in a pub permitted. An admin can't change his own role, but can change
    the role of other admins.
2. Registration. Each user needs an app, so registration only in an app. ???
3. Invitation. A user email must already be registered in the system before he can be invited.

how invitation goes:
admin enters a user email, one at a time; submits
if email in the system, OK
if not, message
URL user/invite
add TemplateView
create a form: email, role