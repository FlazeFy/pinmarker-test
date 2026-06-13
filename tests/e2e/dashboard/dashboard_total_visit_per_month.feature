Feature: Dashboard Page Total Visit Per Month

Scenario: User can see their total visit monthly
    Given I have already signed in to the app
    Then I should see the total visit monthly section title "Total Visit Per Month"
    And I should see the line chart and the horizontal label showing the list of month names
    And I should see a chart with valid values for each series
