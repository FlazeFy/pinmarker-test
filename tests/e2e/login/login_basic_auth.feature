Feature: Login Page Basic Auth

Scenario: User can login with valid data
    Given I open the login page
    Then I should see the section title "Welcome Back"
    And I should see the label "EMAIL OR USERNAME"
    And I should see the label "PASSWORD"
    And I should see the submit button "Sign In"
    When I fill in the email with "jalanjalan"
    And I fill in the password with "admin"
    And I click the submit button
    Then I should be redirected to the dashboard page

Scenario: User cant login with wrong password
    Given I open the login page
    Then I should see the section title "Welcome Back"
    And I should see the label "EMAIL OR USERNAME"
    And I should see the label "PASSWORD"
    And I should see the submit button "Sign In"
    When I fill in the email with "flazen.edu"
    And I fill in the password with "admin4"
    And I click the submit button
    Then I should see alert message "Failed to login To your account. Wrong username or password"

Scenario: User cant login with invalid char length username
    Given I open the login page
    Then I should see the section title "Welcome Back"
    And I should see the label "EMAIL OR USERNAME"
    And I should see the label "PASSWORD"
    And I should see the submit button "Sign In"
    When I fill in the email with "fla"
    And I fill in the password with "admin"
    And I click the submit button
    Then I should see alert message "The Username or Email field must be at least 5 characters in length."

Scenario: User cant login with empty username
    Given I open the login page
    Then I should see the section title "Welcome Back"
    And I should see the label "EMAIL OR USERNAME"
    And I should see the label "PASSWORD"
    And I should see the submit button "Sign In"
    When I fill in the email with " "
    And I fill in the password with "admin"
    And I click the submit button
    Then I should see alert message "The Username or Email field is required."