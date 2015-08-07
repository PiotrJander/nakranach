# Created by piotr at 06.08.15
Feature: Sidebar menu
  # Enter feature description here

  Background:
    Given I am logged in as "Piotr"
    And a pub named "Rademenes"

  Scenario: "Użytkownicy" field is visible for admin pubs
    And I am an admin in Rademenes
    Then sidebar has "Użytkownicy" field with two subfields: "Lista" and "Zaproś"

  Scenario: "Użytkownicy" field is not visible for users who are not admin pubs
    And I am not an admin
    Then sidebar has no "Użytkownicy" field

  Scenario: "Lista kranów" field is visible for employed users
    And I am employed in Rademenes
    Then sidebar has "Lista kranów" field

  Scenario: "Lista kranów" field is not visible for users who don't belong to any pub
    And I am not employed in any pub
    Then sidebar has no "Lista kranów" field
