import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Census Region Mapping
REGION_MAP = {
    'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast', 'NH': 'Northeast', 'RI': 'Northeast', 'VT': 'Northeast',
    'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
    'IL': 'Midwest', 'IN': 'Midwest', 'MI': 'Midwest', 'OH': 'Midwest', 'WI': 'Midwest',
    'IA': 'Midwest', 'KS': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'NE': 'Midwest', 'ND': 'Midwest', 'SD': 'Midwest',
    'DE': 'South', 'FL': 'South', 'GA': 'South', 'MD': 'South', 'NC': 'South', 'SC': 'South', 'VA': 'South', 'WV': 'South',
    'AL': 'South', 'KY': 'South', 'MS': 'South', 'TN': 'South', 'AR': 'South', 'LA': 'South', 'OK': 'South', 'TX': 'South', 'DC': 'South',
    'AZ': 'West', 'CO': 'West', 'ID': 'West', 'MT': 'West', 'NV': 'West', 'NM': 'West', 'UT': 'West', 'WY': 'West',
    'AK': 'West', 'CA': 'West', 'HI': 'West', 'OR': 'West', 'WA': 'West'
}

DATA_DIR = '/data'
OUTPUT_TABLES = '/study/04-analysis/outputs/tables'
OUTPUT_FIGURES = '/study/04-analysis/outputs/figures'

os.makedirs(OUTPUT_TABLES, exist_ok=True)
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

def load_quarter(year, qtr):
    file_path = f"{DATA_DIR}/PBJ_dailynursestaffing_CY{year}Q{qtr}.csv"
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found.")
        return None
    
    cols = ['PROVNUM', 'STATE', 'COUNTY_FIPS', 'CY_Qtr', 'WorkDate', 
            'Hrs_RN', 'Hrs_LPN', 'Hrs_CNA', 
            'Hrs_RN_ctr', 'Hrs_LPN_ctr', 'Hrs_CNA_ctr']
    
    df = pd.read_csv(file_path, usecols=cols, encoding='cp1252', low_memory=False, dtype={'PROVNUM': str})
    
    hour_cols = ['Hrs_RN', 'Hrs_LPN', 'Hrs_CNA', 'Hrs_RN_ctr', 'Hrs_LPN_ctr', 'Hrs_CNA_ctr']
    for col in hour_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

all_years_data = []
strobe_counts = {'initial_rows': 0, 'initial_facilities': 0}

for year in [2022, 2023, 2024]:
    year_dfs = []
    for qtr in [1, 2, 3, 4]:
        df = load_quarter(year, qtr)
        if df is not None:
            strobe_counts['initial_rows'] += len(df)
            year_dfs.append(df)
    
    if not year_dfs:
        continue
        
    year_df = pd.concat(year_dfs)
    
    total_hrs = year_df['Hrs_RN'] + year_df['Hrs_LPN'] + year_df['Hrs_CNA']
    contract_hrs = year_df['Hrs_RN_ctr'] + year_df['Hrs_LPN_ctr'] + year_df['Hrs_CNA_ctr']
    year_df['Contract_Ratio'] = contract_hrs / total_hrs.replace(0, np.nan)
    
    qtr_counts = year_df.groupby('PROVNUM')['CY_Qtr'].nunique()
    valid_facilities = qtr_counts[qtr_counts >= 3].index
    
    strobe_counts[f'fac_less_3_qtrs_{year}'] = year_df['PROVNUM'].nunique() - len(valid_facilities)
    
    year_df = year_df[year_df['PROVNUM'].isin(valid_facilities)]
    
    facility_annual = year_df.groupby(['PROVNUM', 'STATE', 'COUNTY_FIPS']).agg({
        'Contract_Ratio': 'mean'
    }).reset_index()
    
    facility_annual['Year'] = year
    all_years_data.append(facility_annual)

combined_df = pd.concat(all_years_data)

z_scores = stats.zscore(combined_df['Contract_Ratio'], nan_policy='omit')
outliers = np.abs(z_scores) > 4
strobe_counts['outliers_removed'] = outliers.sum()
combined_df = combined_df[~outliers]

county_annual = combined_df.groupby(['STATE', 'COUNTY_FIPS', 'Year']).agg({
    'Contract_Ratio': 'mean'
}).reset_index()

# Descriptive Stats
desc_stats = county_annual.groupby('Year')['Contract_Ratio'].describe()
desc_stats.to_latex(f"{OUTPUT_TABLES}/county_annual_contract_ratios.tex", caption="Descriptive Statistics of Annual County-Level Contract Ratios")

# State-level summaries
state_summaries = county_annual.groupby(['STATE', 'Year'])['Contract_Ratio'].mean().unstack()
state_summaries.index.name = 'State'
state_summaries.to_latex(f"{OUTPUT_TABLES}/state_annual_contract_ratios.tex", caption="Mean Contract Ratio by State and Year")

# Trend Analysis
pivot_county = county_annual.pivot(index=['STATE', 'COUNTY_FIPS'], columns='Year', values='Contract_Ratio')
pivot_county = pivot_county.dropna(subset=[2022, 2024])
pivot_county['Abs_Change'] = pivot_county[2024] - pivot_county[2022]
pivot_county['Pct_Change'] = (pivot_county[2024] - pivot_county[2022]) / pivot_county[2022].replace(0, np.nan) * 100

top_improvement = pivot_county.sort_values('Abs_Change').head(20)
top_decline = pivot_county.sort_values('Abs_Change', ascending=False).head(20)

top_improvement.to_latex(f"{OUTPUT_TABLES}/top_20_counties_improvement.tex", caption="Top 20 Counties with Greatest Reduction in Contract Ratio")
top_decline.to_latex(f"{OUTPUT_TABLES}/top_20_counties_decline.tex", caption="Top 20 Counties with Greatest Increase in Contract Ratio")

# --- Visualizations ---

# Instead of choropleth map (no internet for topojson), use sorted bar charts for state-level data
# 1. State-level 2024 contract ratio
state_2024 = state_summaries[2024].sort_values(ascending=False).reset_index()
plt.figure(figsize=(10, 12))
sns.barplot(data=state_2024, y='State', x=2024, palette='viridis')
plt.title('Mean Contract Staffing Ratio by State (2024)')
plt.xlabel('Contract Ratio')
plt.savefig(f"{OUTPUT_FIGURES}/figure1_state_ratios_2024.png")
plt.close()

# 2. State-level absolute change (2022-2024)
state_change = pivot_county.groupby('STATE')['Abs_Change'].mean().sort_values().reset_index()
plt.figure(figsize=(10, 12))
sns.barplot(data=state_change, y='STATE', x='Abs_Change', palette='RdBu_r')
plt.title('Mean Change in Contract Ratio (2022-2024)')
plt.xlabel('Absolute Change')
plt.savefig(f"{OUTPUT_FIGURES}/figure2_state_change.png")
plt.close()

# 3. Scatter plot: 2022 vs 2024 contract ratio by state
state_trends = state_summaries.reset_index()
plt.figure(figsize=(10, 8))
sns.scatterplot(data=state_trends, x=2022, y=2024)
max_val = max(state_trends[2022].max(), state_trends[2024].max())
plt.plot([0, max_val], [0, max_val], 'r--')
plt.title('State-Level Contract Ratio: 2022 vs 2024')
plt.xlabel('Mean Contract Ratio 2022')
plt.ylabel('Mean Contract Ratio 2024')
for i, txt in enumerate(state_trends['State']):
    plt.annotate(txt, (state_trends[2022].iat[i], state_trends[2024].iat[i]))
plt.savefig(f"{OUTPUT_FIGURES}/figure3_scatter_2022_2024.png")
plt.close()

# 4. Bar chart: Top 10 states by reduction in contract reliance
state_reduction = state_change.head(10)
plt.figure(figsize=(12, 6))
sns.barplot(data=state_reduction, x='STATE', y='Abs_Change', palette='viridis')
plt.title('Top 10 States by Reduction in Contract Staffing Reliance (2022-2024)')
plt.ylabel('Absolute Change in Contract Ratio')
plt.savefig(f"{OUTPUT_FIGURES}/figure4_top_reduction_states.png")
plt.close()

# 5. Line graph: Annual trends by Census Region
county_annual['Region'] = county_annual['STATE'].map(REGION_MAP)
region_trends = county_annual.groupby(['Region', 'Year'])['Contract_Ratio'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=region_trends, x='Year', y='Contract_Ratio', hue='Region', marker='o')
plt.title('Annual Trends in Contract Staffing Ratio by Census Region')
plt.ylabel('Mean Contract Ratio')
plt.xticks([2022, 2023, 2024])
plt.savefig(f"{OUTPUT_FIGURES}/figure5_region_trends.png")
plt.close()

# 6. STROBE flow diagram
plt.figure(figsize=(10, 8))
plt.text(0.5, 0.9, f"Initial Daily Observations (2022-2024)\nn={strobe_counts['initial_rows']:,}", ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))
plt.arrow(0.5, 0.85, 0, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.5, 0.7, f"Facilities excluded (<3 valid quarters/year)\nn={strobe_counts.get('fac_less_3_qtrs_2022', 0) + strobe_counts.get('fac_less_3_qtrs_2023', 0) + strobe_counts.get('fac_less_3_qtrs_2024', 0):,}", ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))
plt.arrow(0.5, 0.65, 0, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.5, 0.5, f"Facility-Year Observations\nn={len(combined_df) + strobe_counts['outliers_removed']:,}", ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))
plt.arrow(0.5, 0.45, 0, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.5, 0.3, f"Outliers excluded (|z| > 4)\nn={strobe_counts['outliers_removed']:,}", ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))
plt.arrow(0.5, 0.25, 0, -0.1, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.5, 0.1, f"Final Analytic Sample (County-Year)\nn={len(county_annual):,}", ha='center', va='center', bbox=dict(boxstyle="round", fc="w"))
plt.axis('off')
plt.savefig(f"{OUTPUT_FIGURES}/strobe_flow.png")
plt.close()

with open('/study/04-analysis/results_summary.md', 'w') as f:
    f.write("# Results Summary: Contract Staffing County Trends (2022-2024)\n\n")
    f.write(f"## Key Statistics\n")
    f.write(f"- Total daily observations processed: {strobe_counts['initial_rows']:,}\n")
    f.write(f"- Final analytic sample: {len(county_annual):,} county-year observations.\n")
    f.write(f"- Outliers removed: {strobe_counts['outliers_removed']:,} facility-year observations.\n\n")
    f.write("## Findings\n")
    f.write("- Analysis suggests varying trends across regions and states.\n")
    f.write("- Detailed tables and figures are available in the outputs directory.\n")

print("Analysis completed successfully.")
