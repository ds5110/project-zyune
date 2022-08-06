import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('./Zipcode/weighted_average_internet_score.csv')

income_internet = sns.regplot(data=df, x='median_household_income',
                              y='weighted_average_internet_score')
fig = income_internet.get_figure()
plt.savefig('./img/income_internet.png')
plt.close()
edu_internet_subscribe = sns.regplot(data=df, x='num_of_bachelor_degree_higer',
                                     y='num_of_internet_subscribe')

fig = edu_internet_subscribe.get_figure()
plt.savefig('./img/edu_internet_subscribe.png')
plt.close()

fig, ax = plt.subplots()


kwargs = {
    'linewidth': 3,  # line width of spot

    # line style of spot
}

ax.scatter(data=df, x='num_of_internet_subscribe',
           y='weighted_average_internet_score', **kwargs)
internet_subscribe_internet_score = sns.regplot(data=df, x="num_of_internet_subscribe", y='weighted_average_internet_score',
                                                scatter=False, ci=20, order=1, color='blue')
fig = internet_subscribe_internet_score.get_figure()
plt.savefig('./img/internet_subscribe_internet_score')
plt.close()
