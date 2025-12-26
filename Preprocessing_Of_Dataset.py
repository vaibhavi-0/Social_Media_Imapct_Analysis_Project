import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('Students Social Media Addiction.csv')
df.head()

df = pd.read_csv('Students Social Media Addiction.csv')
df.head()

# get a summary of the DataFrame, including column names, data types, non-null counts, and memory usage.
df.info()

# Check missing values
df.isnull().sum()

# find the total number of duplicate rows
df.duplicated().sum()

# Binary Label Encoding of Categorical Data
df['Affects_Academic_Performance'] = df['Affects_Academic_Performance'].str.title().str.strip().map({'Yes': 1, 'No': 0})

#  Standardize categorical text
df['Gender'] = df['Gender'].str.strip().str.title()
df['Academic_Level'] = df['Academic_Level'].str.strip().str.title()
df['Country'] = df['Country'].str.strip().str.title()
df['Most_Used_Platform'] = df['Most_Used_Platform'].str.strip().str.title()

#Feature selection remove unwanted or irrelevant columns from a dataset
df = df.drop(['Student_ID', 'Relationship_Status'], axis=1)

df.to_csv('Cleaned_Social_Media_Addiction.csv', index=False)

# EDA
# get a statistical summary
df.describe(include='all')

# Check basic dimensions (no. of rows and clolumns)
df.shape
# Check how many unique (different) values are in each column
df.nunique()

# See how academic performance affects the average of all numeric data
df.groupby("Affects_Academic_Performance").mean(numeric_only=True)

# Group scores into 3 simple levels: Poor (0-4), Moderate (4-6), and Good (6-10)
df["Mental_Health_Level"] = pd.cut(
    df["Mental_Health_Score"],
    bins=[0,4,6,10],
    labels=["Poor","Moderate","Good"]
)

# Show what percentage of people fall into each Mental Health level
df["Mental_Health_Level"].value_counts(normalize=True) * 100

# Compare average scores based on whether social media affects academics
impact_analysis = df.groupby('Affects_Academic_Performance')[['Mental_Health_Score','Avg_Daily_Usage_Hours','Addicted_Score']].mean()
print(impact_analysis.round(2))

# Find the 10 countries with the highest average daily social media usage
print("\n🌍 TOP 10 COUNTRIES BY USAGE")
country_analysis = df.groupby('Country')[['Avg_Daily_Usage_Hours','Mental_Health_Score']].mean().round(2)
print(country_analysis.nlargest(10, 'Avg_Daily_Usage_Hours'))



