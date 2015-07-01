# Created by piotr at 01.07.15
Feature: Pub creation
  Here a user is synonymous with a profile instance.
  E.g. if we say that a user A becomes a pub P admin
  then the Profile A enters a relation with pub P with role admin

  Scenario: Pub creation
    Given A user wants to create a new pub
    When he goes to /pub/create/
    Then he is displayed a pub creation form

  Scenario: Successful pub creation
    Given a user enters valid data in pub creation form
    When he submits the data
    Then the pub is created
    And the user becomes the admin of that pub

  Scenario: Pub already exists
    Too bad.

