import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('../Zipcode/number_of_tiers_cumberlamd_zipcode.csv')
# df = df[df.median_household_income != -666666666]
weighted_average_internet_score_list = []
for index, row in df.iterrows():
    weighted_average_internet_score = (row['num_tier_1']*5+row['num_tier_2']*17.5+row['num_tier_3']
                                       * 37.5+row['num_tier_4']*75+row['num_tier_5']*150)/(5+17.5+37.5+75+150)
    weighted_average_internet_score_list.append(
        weighted_average_internet_score)
print(weighted_average_internet_score_list)

df['weighted_average_internet_score'] = pd.DataFrame(
    weighted_average_internet_score_list)
df['education_rate'] = df['num_of_bachelor_degree_higer']/df['total_population']
df['subscribe_rate'] = df['num_of_internet_subscribe']/df['total_population']
df.to_csv('../Zipcode/weighted_average_internet_score.csv', index=False)
