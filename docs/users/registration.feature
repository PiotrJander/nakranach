# Created by piotr at 01.07.15
Feature: Register a Profile
  User is a person using the site. One user can have many Profiles, but it is highly unlikely.
  Each Profile has a unique email. That email is used to retrieve a gravatar.
  User can register a Profile through the mobile app or the web app.
  In the web app, registration path is /register/.

  Scenario: An unregistered user visits registration page
    Given a user wants to create a Profile
    And she is not logged in
    When she visits /register/
    Then registration form is displayed
    And there are fields: Imię, Nazwisko, Email, Hasło, Potwierdź hasło
    And there are buttons: Zarejestruj się, Powrót do strony logowania

  Scenario: A logged-in user visits registration page
    Given a user wants to create a Profile
    And she is logged in
    When she visits /register/
    Then she is logged out
    And she is directed to registration page

  Scenario: Invalid name
    Given the user enters a name or surname which is not alphanumeric
    When she clicks Zarejestruj się
    Then she is sent back to registration page
    And Invalid name or surname field is marked
    And Warning message is displayed next to the field.
    And The text user entered previously is displayed in the name fields.

  Scenario: Invalid email
    Given the user enters an invalid email
    When she clicks Zarejestruj się
    Then she is sent back to registration page
    And Email field is marked
    And Warning message is displayed next to the field.
    And The text user entered previously is displayed in the name fields.

  Scenario: Password has disallowed characters
    Given the user enters a password which has disallowed characters
    When she clicks Zarejestruj się
    Then she is sent back to registration page
    And Password field is marked
    And Warning message is displayed next to the field
    And Password field is empty

  Scenario: Password is unsafe
    Given the user enters a unsafe password
    When she clicks Zarejestruj się
    Then she is sent back to registration page
    And Password field is marked
    And Warning message is displayed next to the field
    And Password field is empty

  Scenario: Two passwords don't match
    Given the user enters two different passwords
    When she clicks Zarejestruj się
    Then she is sent back to registration page
    And Password field is marked
    And Warning message is displayed next to the field
    And Password field is empty

  Scenario: Successful registration
    Given the user entered valid values
    When she clicks Zarejestruj się
    Then she is send to her dashboard page

  Scenario: User withdraws
    Given the user withdraws from filling the registration form
    When she clicks Powrót do strony logowania
    Then she is sent to login page.