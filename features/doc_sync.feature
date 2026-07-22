Feature: Documentation sync technical profile generation
  As a documentation maintainer
  I want the repository to generate a technical profile report
  So that I can review project structure without manual inspection

  Scenario: Generate a technical profile from a repository
    Given a repository with README, requirements, app, models, routes, and forms files
    When the documentation sync pipeline runs
    Then a technical profile report is created
    And the report contains the project name and technical stack

  Scenario: Missing requirements file uses strict fallbacks
    Given a repository without a requirements.txt file
    When the documentation sync pipeline runs
    Then the report is still created
    And the dependencies section contains Not Specified

  Scenario: Missing route and form details uses strict fallbacks
    Given a repository with no route or form definitions
    When the documentation sync pipeline runs
    Then the report contains Not Specified for routes and forms
