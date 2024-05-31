# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:29:50 2024

@author: jim47
"""

""" Import the necessary libraries"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import seaborn as sns
import plotly.express as px 
import matplotlib.ticker as tick
from scipy.stats import variation
from scipy import stats

""" import the dataset and create the core dataset"""

df = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")

"""Task 3"""
"""1. Create the 'Income_Variability' column"""

df['Income_Variability'] = df['Max_MonthlyIncome'] - df['Min_MonthlyIncome']

""" 2.filter the dataframe"""
""" select groups where the 'Average_YearsAtCompany' are more than the overall median"""

Median_Average_YearsAtCompany = np.median(df.Average_YearsAtCompany)
df_filtered = df.loc[df['Average_YearsAtCompany'] > Median_Average_YearsAtCompany]
df_filtered = df_filtered.reset_index(drop = True)

""" Calculate the'Average_MonthlyIncome' coefficient of variation for the df_filtered"""


def cv(data):
    return np.std(data) / np.mean(data)

Average_MonthlyIncome_CV = df_filtered.groupby(['JobRole', 'Gender'])['Average_MonthlyIncome'].apply(cv)
Average_MonthlyIncome_CV
"""3.Perform t - test between Male and Female 'Average_MonthlyIncome' for the df"""
#We create the two arrays 
Male_MonthlyIncome = df.loc[df['Gender'] == 'Male']['Average_MonthlyIncome']
Female_MonthlyIncome = df.loc[df['Gender'] == 'Female']['Average_MonthlyIncome']

#Then, we perform the analysis
st,p = stats.ttest_ind(Male_MonthlyIncome, Female_MonthlyIncome, equal_var = False)
print(f"T-test results: statistic={st}, pvalue={p}")

"""Spearman rank correlation 'Average_YearsAtCompany' and 'Income_Variability"""
sc,sp = stats.spearmanr(df['Average_YearsAtCompany'],df['Income_Variability'])
print(f"Spearman's correlation: correlation={sc}, pvalue={sp}")

""" 4.Data Aggregation and Transformation"""
#The data must be aggregated by 'EducationField' to derive statistics such as mean, median, and income range.
#We create the aggregated dataframe (df_agg)
income_mean = df.groupby(['EducationField'],as_index = False)['Average_MonthlyIncome'].mean()
income_median = df.groupby(['EducationField'],as_index = False)['Average_MonthlyIncome'].median()
income_max = df.groupby(['EducationField'],as_index = False)['Average_MonthlyIncome'].max()
income_min = df.groupby(['EducationField'],as_index = False)['Average_MonthlyIncome'].min()
df_agg = pd.DataFrame()
df_agg['EducationField'] = income_mean['EducationField']
df_agg['Mean_Income'] = income_mean['Average_MonthlyIncome']
df_agg['Median_Income'] = income_median['Average_MonthlyIncome']
df_agg['Income_Range'] = income_max['Average_MonthlyIncome'] - income_min['Average_MonthlyIncome']
df_agg['Income_Stability'] = [1,1,1,1,1,1]
#Hypothetical income stability formula
for i in range(0,len(df_agg['Income_Range'])):
    if df_agg['Income_Range'][i] == 0:
        df_agg['Income_Stability'][i] = 1
    else:
        df_agg['Income_Stability'][i] = 1/df_agg['Income_Range'][i]

df_agg

"""Task 4: Visual Analysis of Monthly Incomes by Gender and Job Role"""
df_task_four = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")
#we restructure the data using a pivot table
df_task_four['Income_Variability'] = df_task_four['Max_MonthlyIncome'] - df_task_four['Min_MonthlyIncome']
pv = pd.pivot_table(df_task_four, 
                    values = 'Average_MonthlyIncome', index=['JobRole'], 
                    columns = 'Gender')
pv['Female'][1] = 0

# We also need the income variability and average years at company for each category.
var = df_task_four.groupby('JobRole')['Income_Variability'].mean()
avg_years = df_task_four.groupby(['JobRole', 'Gender'])['Average_YearsAtCompany'].mean()

fig_1 = pv.plot(kind='bar',
                title = 'Comparison of Average Monthly Income by Gender per JobRole',
                xlabel = 'Job Role',
                ylabel = 'Average Monthly Income',
                )

""" Task 5: Visualizing Average Monthly Income by Job Role"""
df_task_five = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")
df_agg_t5 = df_task_five.groupby(['JobRole'],as_index = False)['Average_MonthlyIncome'].mean()
#At this point, we create the piechart 
fig_2 = px.pie(df_agg_t5, values='Average_MonthlyIncome',
               names='JobRole', title="Average Monthly Income per Job Role")
# Customize the looks of the pie chart
fig_2.update_traces(
    textposition='outside',
    textinfo='percent+label',
)
fig_2.show()


"""Task 6: Analyzing Monthly Income by Job Role & Education"""
df_task_six = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")
df_agg_t6 = df_task_six.groupby(['EducationField', 'JobRole'], as_index=False)['Average_MonthlyIncome'].mean()
#Creating the plot 
fig_3 = px.line(df_agg_t6, x="JobRole", y="Average_MonthlyIncome", color='EducationField',markers = True,
                title = 'Average Monthly Income per Job across diffrent Education Fields',
                labels={'JobRole':'Job Role',
                        'Average_MonthlyIncome':'Average Monthly Income',
                        'EducationField':'Education Field'})


"""Task 7: Visualizing Monthly Income Distribution by Gender"""
df_task_seven = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")

#We segregate the data based on 'Gender' into two separate series for 'Male' and 'Female', focusing on their 'Average_MonthlyIncome'.
df_AverageIncome_Male = df_task_seven.loc[df_task_seven['Gender'] == 'Male']['Average_MonthlyIncome'].reset_index()

df_AverageIncome_Female = df_task_seven.loc[df_task_seven['Gender'] == 'Female']['Average_MonthlyIncome'].reset_index()

del df_AverageIncome_Male['index']
del df_AverageIncome_Female['index']

#We create the overying histograms
plt.hist(df_AverageIncome_Male, bins=30, alpha=0.5, color='blue', label='Male')  # color parameter is used here
plt.hist(df_AverageIncome_Female, bins=30, alpha=0.5, color='pink', label='Female') 
#Graph formating
plt.xlabel('Average Monthly Income')
plt.ylabel('Frequency')
plt.title('Distribution of Average Monthly Income by Gender')
#Graph Formating
plt.xlabel('Average Monthly Income')
plt.ylabel('Frequency')
plt.title('Distribution of Average Monthly Income by Gender')
plt.legend(title='Gender')
plt.show()

"""Task 8: Exploring the Relationship between Monthly Income and Tenure by Gender"""
df_task_eight = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")
fig_4= px.scatter(df_task_eight,x= 'Average_MonthlyIncome', y= 'Average_YearsAtCompany',color='Gender',
                 title = 'Average Monthly Income VS Average Years at Company for Male and Female Employees',
                 labels = {'Average_MonthlyIncome':'Average Monthly Income',
                          'Average_YearsAtCompany':'Average Years At Company'},
                 hover_data=['JobRole', 'EducationField'],
                 color_discrete_map = {"Male": "SkyBlue", "Female": "Pink"})
fig_4.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
paper_bgcolor='rgba(0, 0, 0, 0)',showlegend=True)
fig_4.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
fig_4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
fig_4.show()

df_agg.to_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\df_agg.csv")
        
        
        
        
