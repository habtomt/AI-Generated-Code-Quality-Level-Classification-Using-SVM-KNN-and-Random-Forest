import pandas as pd

campaign_data = {
    'CampaignID': ['C1', 'C2', 'C3', 'C4'],
    'Spend': [10000, 5000, 20000, 8000],
    'Impressions': [400000, 150000, 800000, 300000],
    'Clicks': [12000, 6000, 25000, 9000],
    'Conversions': [400, 250, 900, 310],
    'Revenue': [35000, 18000, 85000, 28000]
}

df = pd.DataFrame(campaign_data)

df['CTR'] = (df['Clicks'] / df['Impressions']) * 100
df['CR'] = (df['Conversions'] / df['Clicks']) * 100
df['ROI'] = ((df['Revenue'] - df['Spend']) / df['Spend']) * 100
df['CPA'] = df['Spend'] / df['Conversions']

print(df[['CampaignID', 'ROI', 'CTR', 'CR', 'CPA']])