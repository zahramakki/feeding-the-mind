# Feeding the Mind: How Diet Composition Relates to Population Mental Health

**Authors**: Zahra Makki & Susan Hatem

**Datasets**: [Global Dietary Database](https://www.globaldietarydatabase.org/), [Global Mental Health Disorders](https://www.kaggle.com/datasets/thedevastator/global-mental-health-disorders)

---

## Overview

This project explores the relationship between national dietary patterns and mental health outcomes across countries and years. Inspired by emerging research on the gut-brain axis and its influence on behavior and mood, we investigate whether global variations in diet composition correlate with mental health disorder prevalence.

By combining and analyzing data from the Global Dietary Database (GDD) and a global mental health disorders dataset, we engineer composite dietary scores and examine their associations with mental health prevalence using exploratory and correlation-based analysis.

---

## Motivation

The project was inspired by a discussion between Dr. Andrew Huberman and Dr. Diego Bohórquez on the Huberman Lab podcast episode, *The Science of Your Gut Sense & the Gut-Brain Axis*. Their conversation emphasized how gut chemosensation affects food preference, satiety, and mood—suggesting that diet may influence mental health.

Building on this, we aimed to examine the global patterns connecting food consumption with mental health outcomes. While prior studies have found links between specific diets and mental health (e.g., Jacka et al., 2010; Marx et al., 2021), few have explored this relationship at a global scale across multiple decades.

---

## Data Sources

### 1. Global Dietary Database (GDD)
- Source: Global Dietary Database (CSV format)
- Filtered for: National-level data (1990–2017)
- Key Variables: ISO3 (country code), Year, Available dietary factors

### 2. Global Mental Health Disorders
- Source: Kaggle (CSV format)
- Filtered for: Country-level data (1990–2019)
- Key Variables: ISO3 (country code), Year, Prevalence of seven mental health disorders  
  (schizophrenia, bipolar, eating disorders, anxiety, drug use, depression, alcohol use)

---

## Methods

### Data Processing and Cleaning
- Filtered national-level data and harmonized years
- Handled missing values using `missingno` and `seaborn` visualizations
- Converted and normalized values for mental health percentages
- Cleaned and split dietary factors into individual records
- Aligned datasets based on ISO3 and Year

### Feature Engineering
Engineered dietary scores (scaled from 0 to 1):
- **Plant-Based Score**: Proportion of plant-based items in the national diet
- **Animal-Based Score**: Proportion of animal-based items
- **Processed Diet Score**: Ratio of unprocessed to total processed/unprocessed foods
- **Diversity Score**: Number of unique dietary components consumed

### Analysis
- Used Pearson correlation to assess relationships between dietary features and mental health outcomes
- Visualized results using correlation matrices and scatter plots
- Created subsets to maximize usable data (e.g., focused datasets for eating disorders, schizophrenia)

---

## Results

- No strong correlations (r > 0.5) were found between dietary features and mental health outcomes
- **Dietary diversity** and **processed diet score** showed modest correlations with **eating disorders** and **anxiety**
- High data sparsity and inconsistent reporting limited conclusions
- Scatterplots revealed high variability and weak to moderate relationships across all features

---

## Limitations

- Sparse and inconsistent reporting, especially in mental health dataset
- Limited granularity (no age-, gender-, or income-specific data)
- Regional representation was uneven (e.g., North America underrepresented)
- Correlational study; no causal inferences can be drawn

---

## Future Work

- Focus on a specific country or region for more detailed analysis
- Incorporate demographic and socioeconomic variables
- Conduct longitudinal or experimental studies with control and treatment groups
- Implement version control and modular code earlier in the project

---

## Project Structure

```
project-root/
├── data/
│ ├── gdd_cleaned.csv
│ ├── mental_health_cleaned.csv
├── notebooks/
│ ├── analysis.ipynb
│ └── visualizations.ipynb
├── src/
│ ├── scoring.py
│ └── utils.py
├── outputs/
│ ├── correlation_matrices/
│ ├── scatterplots/
│ └── region_distributions/
├── README.md
└── requirements.txt
```

---

## References

- Jacka et al. (2010). *Association of Western and traditional diets with depression and anxiety in women.* [https://doi.org/10.1176/appi.ajp.2009.09060881](https://doi.org/10.1176/appi.ajp.2009.09060881)  
- Marx et al. (2021). *Diet and depression: Exploring the biological mechanisms of action.* [https://doi.org/10.1038/s41380-020-00925-x](https://doi.org/10.1038/s41380-020-00925-x)  
- Huberman Lab Podcast. *The Science of Your Gut Sense & the Gut-Brain Axis.* [http://hubermanlab.com/episode/dr-diego-bohorquez-the-science-of-your-gut-sense-the-gut-brain-axis](http://hubermanlab.com/episode/dr-diego-bohorquez-the-science-of-your-gut-sense-the-gut-brain-axis)  
- Global Burden of Disease (GBD). [https://www.healthdata.org/research-analysis/gbd](https://www.healthdata.org/research-analysis/gbd)
