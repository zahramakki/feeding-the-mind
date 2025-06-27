import pandas as pd
import seaborn as sns
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns

def add_diet_scores(df, plant_based, animal_based, factor_col='factor_set'):
    # Max counts for normalization
    max_plant = len(plant_based)
    max_animal = len(animal_based)

    # Step 1: Compute scores per row
    def compute_scores(factors):
        if not isinstance(factors, set):
            return pd.Series({'plant_based_score': 0, 'animal_based_score': 0})
        plant_count = len(factors & plant_based)
        animal_count = len(factors & animal_based)
        return pd.Series({
            'plant_based_score': plant_count / max_plant if max_plant else 0,
            'animal_based_score': animal_count / max_animal if max_animal else 0
        })

    df[['plant_based_score', 'animal_based_score']] = df[factor_col].apply(compute_scores)
    return df



def compute_processed_diet_score(df: pd.DataFrame, 
                                  factor_column: str,
                                  processed_items: set, 
                                  unprocessed_items: set) -> pd.DataFrame:
    def count_factors(factors):
        if not factors:
            return pd.Series({'processed_count': 0, 'unprocessed_count': 0})
        processed_count = sum(f in processed_items for f in factors)
        unprocessed_count = sum(f in unprocessed_items for f in factors)
        return pd.Series({'processed_count': processed_count, 'unprocessed_count': unprocessed_count})

    # Drop existing columns if they exist to avoid join conflict
    df = df.drop(columns=['processed_count', 'unprocessed_count'], errors='ignore')

    counts = df[factor_column].apply(count_factors)
    df = df.join(counts)

    df['processed_diet_score'] = df.apply(
        lambda row: row['unprocessed_count'] / (row['unprocessed_count'] + row['processed_count'])
        if (row['unprocessed_count'] + row['processed_count']) > 0 else 0, axis=1
    )

    return df

def add_diversity_score(df: pd.DataFrame,
                        factor_col: str,
                        all_factors: set) -> pd.DataFrame:
    """
    Adds a diversity score column to the DataFrame based on unique dietary factors.

    Parameters:
    - df: pd.DataFrame - The input DataFrame
    - factor_col: str - Column name containing sets of dietary factors
    - all_factors: set - Set of all known distinct dietary factors

    Returns:
    - pd.DataFrame - DataFrame with new 'diversity_score' column
    """

    def diversity_score(factors):
        if not factors:
            return 0.0
        return len(factors) / len(all_factors)

    df['diversity_score'] = df[factor_col].apply(diversity_score)
    return df