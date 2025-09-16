import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# Task 1: Load and Explore the Dataset
try:
    # Load Iris dataset
    iris = load_iris(as_frame=True)
    df = iris.frame
    print("First 5 rows of the dataset:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    # Clean the dataset (Iris has no missing values, but let's demonstrate)
    df_clean = df.dropna()
    print(f"\nRows after dropping missing values: {len(df_clean)}")

except FileNotFoundError as fnf_error:
    print(f"File not found: {fnf_error}")
except Exception as e:
    print(f"Error loading or cleaning data: {e}")

# Task 2: Basic Data Analysis
if 'df_clean' in locals():
    print("\nBasic Statistics:")
    print(df_clean.describe())

    # Group by species and compute mean sepal length
    group_mean = df_clean.groupby('target').mean(numeric_only=True)
    print("\nMean values grouped by species (target):")
    print(group_mean)

    # Map species target to actual names for clarity in plots
    df_clean['species'] = df_clean['target'].map(dict(enumerate(iris.target_names)))

    interesting = group_mean['sepal length (cm)']
    print("\nInteresting pattern: Average Sepal Length per Species:")
    for idx, val in interesting.items():
        print(f"{iris.target_names[idx]}: {val:.2f} cm")

    # Task 3: Data Visualization
    sns.set(style="whitegrid")

    # 1. Line Chart: Simulate a time-series (cumulative sum of a feature)
    plt.figure(figsize=(8, 5))
    df_clean['cum_sum'] = df_clean['sepal length (cm)'].cumsum()
    plt.plot(df_clean.index, df_clean['cum_sum'], label='Cumulative Sepal Length')
    plt.title('Cumulative Sepal Length Over Index')
    plt.xlabel('Index')
    plt.ylabel('Cumulative Sepal Length (cm)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 2. Bar Chart: Average Petal Length per Species
    plt.figure(figsize=(7, 4))
    sns.barplot(x='species', y='petal length (cm)', data=df_clean, ci=None, palette="muted")
    plt.title('Average Petal Length per Species')
    plt.xlabel('Species')
    plt.ylabel('Average Petal Length (cm)')
    plt.tight_layout()
    plt.show()

    # 3. Histogram: Distribution of Sepal Width
    plt.figure(figsize=(7, 4))
    plt.hist(df_clean['sepal width (cm)'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Distribution of Sepal Width')
    plt.xlabel('Sepal Width (cm)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    # 4. Scatter Plot: Sepal Length vs. Petal Length
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x='sepal length (cm)', y='petal length (cm)', hue='species', data=df_clean, palette="deep")
    plt.title('Sepal Length vs. Petal Length by Species')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Petal Length (cm)')
    plt.legend(title='Species')
    plt.tight_layout()
    plt.show()
else:
    print("No clean data to analyze or plot.")
