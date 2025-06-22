import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_outcome_correlations(df: pd.DataFrame,
                               outcome_cols: list,
                               feature_cols: list,
                               n_cols: int = 3,
                               cmap: str = 'coolwarm_r',
                               figsize_per_plot: tuple = (5, 4)):
    """
    Plots correlation heatmaps between feature columns and each available outcome column in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - outcome_cols (list): List of potential outcome column names.
    - feature_cols (list): List of feature column names.
    - n_cols (int): Number of columns in the subplot grid.
    - cmap (str): Colormap for heatmap.
    - figsize_per_plot (tuple): Size multiplier for each subplot (width, height).
    """

    # Filter to only outcome columns that are present in the DataFrame
    available_outcomes = [col for col in outcome_cols if col in df.columns]

    n_rows = -(-len(available_outcomes) // n_cols)  # Ceiling division
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * figsize_per_plot[0], n_rows * figsize_per_plot[1]))
    axes = axes.flatten()

    for i, outcome in enumerate(available_outcomes):
        subset_df = df.dropna(subset=[outcome])
        corr_df = subset_df[feature_cols + [outcome]].corr()

        ax = axes[i]
        sns.heatmap(
            corr_df[[outcome]].loc[feature_cols],
            annot=True, cmap=cmap, vmin=-1, vmax=1, ax=ax
        )
        ax.set_title(f'Correlation of {outcome} with Diet Scores')

    # Remove any unused subplots
    for j in range(len(available_outcomes), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()




from scipy.stats import pearsonr

def plot_scatter_with_correlation(df, feature_cols, outcome_cols):
    """
    Plots scatterplots with correlation annotations for each available feature vs each available outcome.

    Parameters:
    - df (pd.DataFrame): DataFrame containing data.
    - feature_cols (list): List of potential feature column names (x-axis).
    - outcome_cols (list): List of potential outcome column names (y-axis).
    """
    available_features = [col for col in feature_cols if col in df.columns]
    available_outcomes = [col for col in outcome_cols if col in df.columns]

    n_rows = len(available_outcomes)
    n_cols = len(available_features)

    if n_rows == 0 or n_cols == 0:
        print("No valid feature-outcome pairs to plot.")
        return

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4), squeeze=False)

    for row, outcome in enumerate(available_outcomes):
        for col, feature in enumerate(available_features):
            ax = axes[row][col]

            # Drop rows with missing data and coerce types to numeric
            subset_df = df[[feature, outcome]].dropna()
            subset_df[feature] = pd.to_numeric(subset_df[feature], errors='coerce')
            subset_df[outcome] = pd.to_numeric(subset_df[outcome], errors='coerce')
            subset_df = subset_df.dropna()

            if subset_df.empty:
                ax.set_title(f"No data: {feature} vs {outcome}")
                ax.axis('off')
                continue

            sns.scatterplot(data=subset_df, x=feature, y=outcome, ax=ax)

            # Calculate Pearson correlation
            r, p = pearsonr(subset_df[feature], subset_df[outcome])
            annotation = f"r = {r:.2f}\n(p = {p:.3f})"
            ax.annotate(annotation, xy=(0.05, 0.95), xycoords='axes fraction',
                        fontsize=12, ha='left', va='top', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray"))

            if row == 0:
                ax.set_title(feature)
            if col == 0:
                ax.set_ylabel(outcome)
            else:
                ax.set_ylabel('')
            ax.set_xlabel(feature)
            ax.grid(True)

    plt.tight_layout()
    plt.show()


def plot_country_distribution(df: pd.DataFrame, 
                               title: str = "Country Distribution", 
                               top_n: int = None, 
                               min_count: int = 1):
    """
    Plots a histogram of ISO3 country code distribution in the DataFrame with dynamic scaling and filtering.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing an 'ISO3' column.
    - title (str): Title for the plot.
    - top_n (int, optional): If specified, only the top N most frequent countries will be shown.
    - min_count (int): Minimum number of records required to include a country.
    """
    if 'ISO3' not in df.columns:
        print("The DataFrame does not contain an 'ISO3' column.")
        return

    country_counts = df['ISO3'].value_counts()
    country_counts = country_counts[country_counts >= min_count]

    if country_counts.empty:
        print("No countries meet the minimum count threshold.")
        return

    if top_n is not None:
        country_counts = country_counts.head(top_n)

    num_countries = len(country_counts)
    height_per_country = 0.4  # Adjust if necessary
    fig_height = max(4, num_countries * height_per_country)

    plt.figure(figsize=(10, fig_height))
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='Blues_r')
    plt.xlabel("Number of Records")
    plt.ylabel("Country (ISO3)")
    plt.title(title)
    plt.tight_layout()
    plt.show()




def plot_region_distribution(df: pd.DataFrame,
                             iso3_col: str = 'ISO3',
                             region_map: dict = None,
                             title: str = "Regional Distribution"):
    """
    Plots a histogram showing the distribution of records by region.

    Parameters:
    - df (pd.DataFrame): DataFrame with a column of ISO3 country codes.
    - iso3_col (str): The name of the column containing ISO3 codes.
    - region_map (dict): Mapping from ISO3 codes to regions.
    - title (str): Title of the plot.
    """
    if region_map is None:
        print("You must provide a region mapping (ISO3 -> Region).")
        return
    if iso3_col not in df.columns:
        print(f"'{iso3_col}' column not found in DataFrame.")
        return

    # Map ISO3 to regions
    df['Region'] = df[iso3_col].map(region_map)

    # Count valid (non-null) region entries
    region_counts = df['Region'].value_counts().sort_values(ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_counts.values, y=region_counts.index, palette='Blues_r')
    plt.xlabel("Number of Records")
    plt.ylabel("Region")
    plt.title(title)
    plt.tight_layout()
    plt.show()

    # Optional: Return the counts for inspection
    return region_counts



def normalize_outcome_columns(df):
    outcome_cols = ['schizophrenia', 'bipolar', 'eating_disorder', 
                    'anxiety', 'drug_use', 'depression', 'alcohol_use']
    
    # Work on a copy to avoid modifying original df
    df_cleaned = df.copy()
    
    for col in outcome_cols:
        if col in df_cleaned.columns:
            # Convert to numeric (non-numeric becomes NaN)
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
            
            # Drop obviously invalid values (e.g. raw counts)
            df_cleaned.loc[df_cleaned[col] > 100, col] = np.nan
            
            # Convert percentages (1-100) to proportion
            mask = (df_cleaned[col] > 1) & (df_cleaned[col] <= 100)
            df_cleaned.loc[mask, col] = df_cleaned.loc[mask, col] / 100
            
            # Keep values between 0 and 1 as-is
            # Invalid negative values also set to NaN
            df_cleaned.loc[df_cleaned[col] < 0, col] = np.nan
        else:
            print(f"{col} not found in dataframe, skipping.")
    
    return df_cleaned

