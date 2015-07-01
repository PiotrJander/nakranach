# Created by piotr at 01.07.15
Feature: Inviting users to pubs
  Here to invite a user means to offer him to enter an ProfilePub relation with the pub.

  Scenario: Viewing the invitation form
    Given a pub admin wants to invite a group of users to work in the pub
    When she visits /users/invite/
    Then she is presented a form allowing her to invite a number of users by email
    And the form consists of a number of rows, where a row represents the user to be invited
    And a row has fields: Email, Rola (choose from Admin / Barman / Pracownik magazynu)

  Scenario: Filling the invitation form
    Given the pub admin has filled the invitation form with user emails and chose their roles
    When she submits the form
    Then she is redirected to a confirmation page at /users/invite/confirm/

  Scenario: User emails already in the system
    Given a number of invited emails are already in the system
    When the pub admin views the confirmation page
    Then those emails are listed together
    And the admin is informed that those users will be offered to join the pub

  Scenario: User emails not yet in the system
    Given a number of invited emails are not yet in the system
    When the pub admin views the confirmation page
    Then those emails are listed together
    And the admin is asked to proofread the emails
    And the admin is informed that emails are not yet registered but will be invited by email

  Scenario: Invitation confirmed
    Given pub admin is viewing the confirmation page
    When she confirms the invitation
    Then users are sent an invitation by email
    And unregistered users are asked to register at Nakranach by email
    And registered users, when they log in, are asked if they want to accept the invitation

  Scenario: Registration after invitation
    Given a user registers at Nakranach after he was invited by email to join a pub
    When he creates a Profile at Nakranach and logs to the web app
    Then he is asked if he wants to accept the invitation

  Scenario: Correcting invitation
    Given the pub admin wants to correct the invitation
    And possibly because she notices an email is incorrect
    Then she is redirected to /user/invite/
    And the form is filled with the data she entered previously