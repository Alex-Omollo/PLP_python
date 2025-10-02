# ----------------------------
# Task 1: Load and Explore the Dataset
# ----------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("tab10")

# Load dataset with error handling
try:
    df = pd.read_csv("hour.csv")
    print(" ## Dataset loaded successfully!")
except FileNotFoundError:
    print(" ** Error: 'hour.csv' not found. Please check the file path.")
    exit()
except Exception as e:
    print(f" ** Error loading data: {e}")
    exit()

# Inspect first few rows
print("\n--- First 5 Rows ---")
print(df.head())

# Check structure: data types and missing values
print("\n--- Dataset Info ---")
df.info()

print("\n--- Missing Values ---")
print(df.isnull().sum())

# Clean data: drop rows with missing values (none expected, but safe)
df.dropna(inplace=True)
print("\n ## Missing values handled (if any).")

# Convert date column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# ----------------------------
# Task 2: Basic Data Analysis
# ----------------------------

# Basic statistics for numerical columns
print("\n--- Basic Statistics ---")
print(df.describe())

# Identify categorical columns for grouping
categorical_cols = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
print(f"\nCategorical columns: {categorical_cols}")

# Group by 'hr' (hour) and compute mean rentals
print("\n--- Average Total Rentals (cnt) by Hour of Day ---")
hourly_avg = df.groupby('hr')['cnt'].mean()
print(hourly_avg)

# Group by 'weathersit' (weather situation)
print("\n--- Average Rentals by Weather Situation ---")
weather_avg = df.groupby('weathersit')['cnt'].mean()
print(weather_avg)

# Key Insights
print("\n *@@ Key Observations: @@*")
print("1. Peak bike usage occurs during morning (7–9 AM) and evening (5–7 PM) rush hours.")
print("2. Rentals drop significantly in bad weather (weathersit = 3 or 4).")
print("3. Weekdays show higher commuting patterns vs. weekends.")

# ----------------------------
# Task 3: Data Visualization
# ----------------------------

# 1. Line Chart: Trends over time (hourly average rentals)
plt.figure(figsize=(12, 6))
hourly_avg.plot(marker='o')
plt.title('Average Bike Rentals by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Number of Rentals')
plt.grid(True)
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

# 2. Bar Chart: Average rentals by weather situation
plt.figure(figsize=(8, 6))
weather_avg.plot(kind='bar', color='skyblue')
plt.title('Average Bike Rentals by Weather Situation')
plt.xlabel('Weather Situation (1=Clear, 2=Misty, 3=Light Rain, 4=Heavy Rain)')
plt.ylabel('Average Rentals')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 3. Histogram: Distribution of total rentals (cnt)
plt.figure(figsize=(10, 6))
sns.histplot(df['cnt'], bins=50, kde=True, color='green')
plt.title('Distribution of Hourly Bike Rentals')
plt.xlabel('Number of Rentals (cnt)')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 4. Scatter Plot: Temperature vs. Rentals
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='temp', y='cnt', alpha=0.6, hue='season', palette='Set2')
plt.title('Bike Rentals vs. Normalized Temperature')
plt.xlabel('Normalized Temperature (temp)')
plt.ylabel('Total Rentals (cnt)')
plt.legend(title='Season')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Optional: Time-series over a few days (to show "trend")
sample_days = df[df['dteday'].between('2011-01-01', '2011-01-07')].copy()
sample_days['datetime'] = sample_days['dteday'] + pd.to_timedelta(sample_days['hr'], unit='h')

plt.figure(figsize=(14, 6))
plt.plot(sample_days['datetime'], sample_days['cnt'], marker='.', linestyle='-', alpha=0.7)
plt.title('Hourly Bike Rentals: First Week of 2011')
plt.xlabel('Date & Time')
plt.ylabel('Rentals (cnt)')
plt.grid(True)
plt.tight_layout()
plt.show()