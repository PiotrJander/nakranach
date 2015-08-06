# Created by piotr at 06.08.15
Feature: Sidebar menu
  # Enter feature description here

  Background:
    Given a user named "Piotr"
    And a pub named "Rademenes"

  Scenario: Piotr is a pub admin and looks for "Użytkownicy" field
    Given I am logged in as Piotr
    And I am an admin in Rademenes
    When I look at the sidebar menu
    Then there is an "Użytkownicy" field with two subfields: "Lista" and "Zaproś"

  Scenario: Piotr is not a pub admin and looks for "Użytkownicy" field
    Given I am logged in as Piotr
    And I am not an admin
    When I look at the sidebar menu
    Then there is no "Użytkownicy" field

  Scenario: Piotr is employed in Rademenes and looks for "Lista kranów" field
    Given I am logged in as Piotr
    And I am employed in Rademenes
    When I look at the sidebar menu
    Then there is a "Lista kranów" field

  Scenario: Piotr is not employed in any pub and looks for "Lista kranów" field
    Given I am logged in as Piotr
    And I am not employed in any pub
    When I look at the sidebar menu
    Then there is no "Lista kranów"

# wouldn't it be simplier to say: "Lista kranów" is only displayed if a user is in a pub?
# we could test that in a unit test, passing a request to SidebarMenu constructor.