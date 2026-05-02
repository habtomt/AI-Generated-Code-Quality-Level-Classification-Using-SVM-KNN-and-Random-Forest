"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_002.txt
Run      : 1
"""

import numpy as np

class MarketingCampaignEvaluator:
    def __init__(self, campaign_data):
        # campaign_data should be a list of dictionaries with the following keys:
        # - campaign_id: Identifier for the campaign
        # - cost: Total cost of the campaign
        # - conversions: Number of conversions from the campaign
        # - revenue: Total revenue generated from the campaign
        # - engagements: Total number of customer engagements (likes, shares, clicks, etc.)
        self.data = campaign_data

    def evaluate(self):
        results = []
        for campaign in self.data:
            try:
                conversion_rate = self.calculate_conversion_rate(campaign['conversions'], campaign['engagements'])
                roi = self.calculate_roi(campaign['revenue'], campaign['cost'])
                engagement_rate = self.calculate_engagement_rate(campaign['engagements'], campaign['cost'])
                results.append({
                    'campaign_id': campaign['campaign_id'],
                    'conversion_rate': conversion_rate,
                    'roi': roi,
                    'engagement_rate': engagement_rate
                })
            except KeyError as e:
                print(f"Error: Missing key {e} in campaign data.")
            except ZeroDivisionError:
                print("Error: Division by zero encountered in calculations.")
        return results

    def calculate_conversion_rate(self, conversions, engagements):
        # Calculate the conversion rate as a percentage.
        return (conversions / engagements) * 100 if engagements > 0 else 0

    def calculate_roi(self, revenue, cost):
        # Calculate the return on investment.
        return ((revenue - cost) / cost) * 100 if cost > 0 else 0

    def calculate_engagement_rate(self, engagements, cost):
        # Calculate the engagement rate per dollar spent.
        return engagements / cost if cost > 0 else 0

if __name__ == '__main__':
    # Example data
    campaign_data = [
        {'campaign_id': '1', 'cost': 1000, 'conversions': 50, 'revenue': 5000, 'engagements': 2000},
        {'campaign_id': '2', 'cost': 1500, 'conversions': 75, 'revenue': 7500, 'engagements': 3000},
        {'campaign_id': '3', 'cost': 2000, 'conversions': 100, 'revenue': 10000, 'engagements': 4000},
    ]

    evaluator = MarketingCampaignEvaluator(campaign_data)
    evaluation_results = evaluator.evaluate()

    for result in evaluation_results:
        print(f"Campaign ID: {result['campaign_id']}")
        print(f"Conversion Rate: {result['conversion_rate']:.2f}%")
        print(f"ROI: {result['roi']:.2f}%")
        print(f"Engagement Rate: {result['engagement_rate']:.2f} engagements per dollar")
        print("-" * 50)