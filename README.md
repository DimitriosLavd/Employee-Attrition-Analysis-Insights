# Employee Attrition Analysis and Insights

## Table of Contents 

- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Tools](#tools)
- [Task 1 and 2 - SQL query and Data Extraction](#task-1-and-2---sql-query-and-data-extraction)
- [Task 3 - Comprehensive Data Analysis and Interpretation](#task-3---comprehensive-data-analysis-and-interpretation)
- [Task 4 - Visual Analysis of Monthly Incomes by Gender and Job Role](#task-4---visual-analysis-of-monthly-incomes-by-gender-and-job-role)
- [Task 5 - Visualizing Average Monthly Income by Job Role](#task-5---visualizing-average-monthly-income-by-job-role)
- [Task 6 - Analyzing Monthly Income by Job Role and Education](#task-6---analyzing-monthly-income-by-job-role-and-education)
- [Task 7 - Visualizing Monthly Income Distribution by Gender](#task-7---visualizing-monthly-income-distribution-by-gender)
- [Task 8 - Exploring the Relationship between Monthly Income and Tenure by Gender](#task-8---exploring-the-relationship-between-monthly-income-and-tenure-by-gender)
- [Conclusion](#conclusion)
- [Refrences](#refrences)



### Project Overview 

In this project we perform intricate examination of employee datasets, through nuanced **SQL** querying and sophisticated **Python**-driven analytics to decipher underlying patterns and emergent insights.Our main objectives are the following:

- Extract specific subsets of data using SQL.
- Implement Python for data computations.
- Engage libraries like pandas, numpy, matplotlib, seaborn, and plotly for thorough data scrutiny and visual presentations.

### Data Sources 

Our main data source is the emp_attrition.csv that was provided by the [Machine Learning and AI Bootcamp](https://academy.workearly.services/course/machine-learning-and-ai-bootcamp)

### Tools 

- WPS Sheets - Preliminary Data Inspection
- Big Query Sandbox (SQL) - Extracting specific subsets
- Anaconda Navigator/Spyder (Python) - Data Analysis, Data Computations, Data Visualizations

### Task 1 and 2 - SQL query and Data Extraction

Our initial dataset contains information about 1470 employees. You can see our initial dataset in the "emp_attrition.csv" file

We wannt to extract insights about employees with moderate to low job satisfaction levels (JobSatisfaction <= 3) in the company's dataset. The column of interest are the following: JobRole: The specific role of the employee in the company.

- Gender: Gender of the employee (Male or Female).
- EducationField: Field of study or specialization.
- Average_MonthlyIncome: Average monthly income for the grouped categories.
- Max_MonthlyIncome: Highest monthly income observed for the grouped categories.
- Min_MonthlyIncome: Lowest monthly income observed for the grouped categories.
- Average_YearsAtCompany: Average number of years these employees have been with the company.
- Employee_Count: The number of employees in each grouped category.

We also considered the following conditions:

- The query focuses only on employees who have a job satisfaction level of 3 or less.
- Grouping is done based on the combination of JobRole, Gender, and EducationField.
- Only groups with more than 5 employees (Employee_Count > 5) are considered in the result.

We extracted the specific subset, using the following SQL Query: 

``` sql
SELECT
  *
FROM (
  SELECT
    JobRole,
    Gender,
    EducationField,
    AVG(MonthlyIncome) AS Average_MonthlyIncome,
    MAX(MonthlyIncome) AS Max_MonthlyIncome,
    MIN(MonthlyIncome) AS Min_MonthlyIncome,
    AVG(YearsAtCompany) AS Average_YearsAtCompany,
    COUNT(*) AS Employee_Count
  FROM
    `attrition.information`
  WHERE
    JobSatisfaction <= 3
  GROUP BY
    JobRole,
    Gender,
    EducationField)
WHERE
  Employee_Count >5
```

### Task 3 - Comprehensive Data Analysis and Interpretation

At this point, we had produced the final dataset, and we stored as 'sample.csv'. The required script we have to concoct involves importing required data science libraries and performing a multi-step analysis on a dataset, specifically focusing on income and tenure-related insights. The aim is to ensure data integrity, carry out statistical analysis, and aggregate data to derive meaningful interpretations.

Step 1: Data Loading and Preprocessing:

- The script begin by importing necessary Python libraries.
- The dataset, named 'sample.csv', is read into a Pandas DataFrame.
- A new column, 'Income_Variability', is  created to capture the difference between the maximum and minimum incomes.

The python script is the following: 

```python
""" Import the necessary libraries"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import seaborn as sns
import plotly.express as px 
import matplotlib.ticker as tick
from scipy.stats import variation
from scipy import stats

""" we import the dataset and create the core dataset"""
df = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")

"""we reate the 'Income_Variability' column"""
df['Income_Variability'] = df['Max_MonthlyIncome'] - df['Min_MonthlyIncome']
```

Step 2: Advanced Filtering and Computation

- Groups in which the 'Average_YearsAtCompany' is above the overall median is filtered.
- For the selected groups, the coefficient of variation for 'Average_MonthlyIncome' is calculated.

The python script is the following: 

``` python

""" we select groups where the 'Average_YearsAtCompany' are more than the overall median"""
Median_Average_YearsAtCompany = np.median(df.Average_YearsAtCompany)
df_filtered = df.loc[df['Average_YearsAtCompany'] > Median_Average_YearsAtCompany]
df_filtered = df_filtered.reset_index(drop = True)

""" we calculate the'Average_MonthlyIncome' coefficient of variation for the df_filtered"""
def cv(data):
    return np.std(data) / np.mean(data)

Average_MonthlyIncome_CV = df_filtered.groupby(['JobRole', 'Gender'])['Average_MonthlyIncome'].apply(cv)
Average_MonthlyIncome_CV
```

step 3: Statistical Analysis

- We coduct a hypothesis testing to compare 'Average_MonthlyIncome' between 'Male' and 'Female' groups using Welch's t-test.
- We carry out a Spearman's rank correlation test between 'Average_YearsAtCompany' and 'Income_Variability'.

```python

"""We perform t - test between Male and Female 'Average_MonthlyIncome' for the df"""
#We create the two arrays 
Male_MonthlyIncome = df.loc[df['Gender'] == 'Male']['Average_MonthlyIncome']
Female_MonthlyIncome = df.loc[df['Gender'] == 'Female']['Average_MonthlyIncome']

#Then, we perform the analysis
st,p = stats.ttest_ind(Male_MonthlyIncome, Female_MonthlyIncome, equal_var = False)
print(f"T-test results: statistic={st}, pvalue={p}")

"""Spearman rank correlation 'Average_YearsAtCompany' and 'Income_Variability"""
sc,sp = stats.spearmanr(df['Average_YearsAtCompany'],df['Income_Variability'])
print(f"Spearman's correlation: correlation={sc}, pvalue={sp}")
```

step 4: Data Aggregation and Transformation:

- The data must be aggregated by 'EducationField' to derive statistics such as mean, median, and income range.
- A hypothetical 'Income_Stability' index is formulated and calculated.

We have the following python code: 

```python
""" Data Aggregation and Transformation"""
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
```

By following the previous steps, we generated the following results: 

1️⃣ Coefficient of Variation across Job Roles and Gender.This metric highlights the relative variability of Average_MonthlyIncome across different job roles and genders:

Healthcare Representative:
Female: 9.93%
Male: 4.86%

Manager:
Female: 0.40%
Male: 0.16%

Manufacturing Director:
Female: 6.60%
Male: 0.00%

Research Director:
Female: 0.31%
Male: 2.92%

Research Scientist:
Female: 0.00%

Sales Executive:
Female: 5.86%
Male: 10.74%

2️⃣ T-test Results for Gender-wise Average Monthly Income:
T-statistic: -0.137
P-value: 0.892
Interpratation: The p-value is significantly higher than the usual alpha level (e.g., 0.05). This suggests that there's no statistically significant difference in the Average_MonthlyIncome between males and females.

3️⃣ Spearman Correlation between Years at Company and Income Variability:
Correlation Coefficient: 0.704
P-value: 3.47 x 10⁻⁸
Interpretation: With a strong positive correlation of 0.704 and a very low p-value, there's a significant association between Average_YearsAtCompany and Income_Variability. This indicates that as the average years at the company increase, income variability also tends to increase.

4️⃣ Aggregated Statistics by Education Field:
Dive into the metrics derived for various education fields:

|FIELD1|EducationField|Mean_Income      |Median_Income|Income_Range          |Income_Stability|
|------|--------------|-----------------|-------------|----------------------|----------------|
|0     |Human Resources|3441.0           |3441.0       |0.0                   |1.0             |
|1     |Life Sciences |8068.652433544805|7212.248717948718|15023.472222222223    |6.656250866699331e-05|
|2     |Marketing     |4812.543452380953|4714.628571428571|4734.416666666668     |0.0002112192631968035|
|3     |Medical       |7969.295772098559|6495.9958333333325|14890.54545454546     |6.715670712349506e-05|
|4     |Other         |4333.284090909091|3830.0       |2510.3977272727275    |0.00039834325419278906|
|5     |Technical Degree|5270.105390641104|3117.111111111111|6511.452380952378     |0.00015357556832101688|

### Task 4 - Visual Analysis of Monthly Incomes by Gender and Job Role

Objective: The objective of this task is to visually represent a comparison of average monthly incomes categorized by gender and job roles. The visual representation should use bar charts, accompanied by additional information such as income variability and average years at the company. We create the graph using the following code:

```python
"""Visual Analysis of Monthly Incomes by Gender and Job Role"""
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
```

![image](https://github.com/DimitriosLavd/Employee-Attrition-Analysis-Insights/assets/157892523/99c80ecc-9f43-460a-b799-86cc2d32dd6c)

### Task 5 - Visualizing Average Monthly Income by Job Role

Objective: The purpose of this task is to create an interactive pie chart that represents the average monthly incomes distributed across various job roles. This visual will provide an at-a-glance view of the income distribution among the roles.In essence, this task is about translating raw data on average monthly incomes into a visual narrative. The resulting interactive pie chart should empower viewers to quickly grasp the relative distribution of incomes among different job roles. Proper execution of this task will make complex data more accessible and interpretable. We created the graph using the following code: 

``` python
""" Visualizing Average Monthly Income by Job Role"""
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
```

![image](https://github.com/DimitriosLavd/Employee-Attrition-Analysis-Insights/assets/157892523/229ae34c-e9fe-45a9-9a35-325f81785046)

### Task 6 - Analyzing Monthly Income by Job Role and Education

Objective: The main goal of this task is to visualize the interplay between 'JobRole', 'EducationField', and 'Average_MonthlyIncome'. The resulting line chart will enable a viewer to discern the average monthly income for various job roles and understand how this varies based on one's educational background. We created the releavant graph using the following code: 

```python
"""Task 6: Analyzing Monthly Income by Job Role & Education"""
df_task_six = pd.read_csv("D:\data analysis_2\Case Studies\Employee Attrition Analysis & Insights\samples.csv")
df_agg_t6 = df_task_six.groupby(['EducationField', 'JobRole'], as_index=False)['Average_MonthlyIncome'].mean()
#Creating the plot 
fig_3 = px.line(df_agg_t6, x="JobRole", y="Average_MonthlyIncome", color='EducationField',markers = True,
                title = 'Average Monthly Income per Job across diffrent Education Fields',
                labels={'JobRole':'Job Role',
                        'Average_MonthlyIncome':'Average Monthly Income',
                        'EducationField':'Education Field'})
```

![image](https://github.com/DimitriosLavd/Employee-Attrition-Analysis-Insights/assets/157892523/8fe53215-293b-4f3d-a52f-15f3bfa9d351)

### Task 7 - Visualizing Monthly Income Distribution by Gender

Objective: To gain insights into the distribution of average monthly incomes among different genders, this task aims to create an overlaid histogram that distinctly represents the income frequencies for males and females.This task revolves around crafting a comprehensive visualization to decode the intricacies of average monthly incomes across genders. When executed meticulously, it will not only offer a clear visual summary but also instigate informed discussions on potential income disparities. We created the following graph with the code bellow:

```python
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
```

![image](https://github.com/DimitriosLavd/Employee-Attrition-Analysis-Insights/assets/157892523/09812b5e-5167-4c6d-87d6-74dedb02d445)

### Task 8 - Exploring the Relationship between Monthly Income and Tenure by Gender

Objective: The primary intent of this task is to visually explore and showcase the relationship between employees' average monthly incomes and their average tenure at the company. A secondary goal is to discern patterns by gender using an interactive scatter plot adorned with a dark theme.In sum, this task elegantly weaves data visualization with interactivity, offering a comprehensive exploration of monthly incomes and company tenures, segmented by gender. Properly executed, it will serve as an insightful tool, fostering informed dialogues about potential income and tenure trends within the organization.

```python
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
```

![image](https://github.com/DimitriosLavd/Employee-Attrition-Analysis-Insights/assets/157892523/24564722-660c-46dc-aab0-f1eda640dcbe)

### Conclusion

🔍 Overview:

Throughout our journey, we delved deep into various visualization tasks, each distinct in its approach and objective. These tasks allowed us to effectively harness Python's capabilities, combined with libraries like pandas, plotly.express, and matplotlib, to extract, process, and visually interpret multifaceted datasets.

Key Highlights:

1. Income Disparity Visualization:

 - We embarked on a mission to unravel potential income disparities across different job roles. Through a pie chart, we uncovered the average monthly income for each role, offering stakeholders a clear 
   picture of the financial landscape within the organization.

2. Tenure and Income Analysis:

- Shifting our lens towards educational backgrounds, we painted a vibrant line chart. It juxtaposed job roles and average monthly incomes, further segmented by education fields. This meticulous breakdown 
  illuminated the influence of educational backgrounds on income levels within job roles.
3. Income Distribution by Gender:

- With gender equality being a central theme, we designed histograms to delve into the average monthly income distribution between males and females. This task accentuated the importance of assessing and 
  rectifying potential gender-based income imbalances.
  
4. Relationship Mapping:

 - Our final visualization was a dark-themed scatter plot, which aesthetically showcased the correlation between employees' monthly incomes and their tenure at the company. This dynamic visual emphasized 
   the intricate interplay of income, years spent at the company, and gender.

🌟 Final Thoughts:

These visualization tasks are not mere standalone exercises but interconnected threads weaving a comprehensive narrative. When taken collectively, they provide holistic insights into the organization's financial dynamics, employee demographics, and potential areas of focus. They underscore the power of data visualization in catalyzing informed discussions and decision-making.

While each visualization answered specific questions, they collectively set the stage for broader dialogues about income disparities, gender equality, and employee career trajectories. It's crucial to harness these insights, ensuring they pave the way for actionable strategies, fostering a more inclusive and balanced organizational culture.

In conclusion, visualizations are a bridge between raw data and actionable insights. By meticulously designing and interpreting these visuals, we empower stakeholders to navigate complex datasets, sparking conversations, and inspiring change.

### Refrences 

1. [Workearly Machine Learning & AI Bootcamp](https://academy.workearly.services/course/machine-learning-and-ai-bootcamp)
2. [Python](https://www.python.org/)
3. [Pandas](https://pandas.pydata.org/)
4. [NymPy](https://numpy.org/)
5. [Plotly](https://plotly.com/python/)
6. [Seaborn](https://seaborn.pydata.org/)





















