Feature: Dashboard Page Main Category Distribution

Scenario: User can see their marker main category distribution
    Given I have already signed in to the app 
    Then I should see the labels "Culinary Spots, Entertainments, Others"
    Then I should see the value for each main category distribution