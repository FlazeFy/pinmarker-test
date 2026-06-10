Feature: Dashboard Page Summary

Scenario: User can see their summary
    Given I have already signed in to the app 
    Then I should see the summary section title "SUMMARY"
    And I should see the summary labels "Total Markers, Favorite Pins, Most Visit, Top Category"
    And the counters should contain numeric values