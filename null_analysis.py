import pandas as pd
import seaborn as sns
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns

def plot_msno_heatmap(df):
    msno.heatmap(df)
    plt.show()

def plot_sns_heatmap(df):
    sns.heatmap(df.isna(), cbar=False, cmap='viridis')
    plt.title('NaN Value Heatmap')
    plt.show()

def nan_count(df):
    print("Count of NaN values per column:")
    print(df.isna().sum())

def nan_percent(df):
    print("\nPercentage of NaN values per column:")
    print(gdd_df.isna().mean() * 100)