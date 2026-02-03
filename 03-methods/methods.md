# Methodology

This study employs a longitudinal analysis of nursing home contract staffing levels across United States counties from 2022 to 2024. The methodology focuses on data cleaning, multi-level aggregation, and robust statistical trend analysis.

## Data Source and Preparation

The primary data source is the CMS Payroll-Based Journal (PBJ) system, which provides daily, facility-level staffing hours by job category and contract status.

### Annual Aggregation Process

The aggregation from daily PBJ records to annual county-level means follows a three-step hierarchy:

1.  **Quarterly Cleaning**: Daily facility records are aggregated to calendar quarters. During this stage, facilities meeting CMS aberrant staffing criteria (e.g., total nurse staffing = 0 or > 12 hours per resident day) are flagged for exclusion.
2.  **Annual Facility Level**: Quarterly averages are calculated for each facility to produce annual estimates. Facilities must have at least three valid quarters of data to be included in the annual average to ensure representativeness and reduce seasonal bias.
3.  **County Aggregation**: Annual facility-level metrics are aggregated to the county level using arithmetic means. Counties with fewer than three reporting facilities are flagged or excluded from the primary trend analysis to ensure the stability of the mean and protect against disclosure risk in small samples.

### Outlier Screening

To ensure the robustness of the results, we apply a strict outlier removal protocol prior to aggregation:
- **Z-Score Threshold**: Any facility-year observation with a Z-score absolute value greater than 4 (|z| > 4) for continuous variables is excluded.
- **Applied Variables**: This rule is specifically applied to 'Contract Ratio' and 'Total Nursing Hours per Resident Day'.
- **Rationale**: This threshold removes extreme anomalies while preserving the natural variance in staffing patterns across different facility types and regions.

## Statistical Approach

### Trend Analysis (2022-2024)

The primary analysis examines the temporal shifts in contract staffing dependence:
- **Descriptive Statistics**: We report means, standard deviations, and quartiles for contract ratios by year.
- **Linear Trend Modeling**: A linear mixed-effects model is used to estimate the average annual change in contract ratios, with counties treated as random effects to account for spatial clustering and repeated measures.
- **Comparison**: Changes between 2022 (baseline) and 2024 (end-of-period) are tested for statistical significance using paired t-tests for county means.

## STROBE Flow Diagram Steps

The study population flow is documented following the STROBE (Strengthening the Reporting of Observational Studies in Epidemiology) guidelines:

1.  **Initial Sample**: Total number of unique Medicare/Medicaid-certified nursing facilities reporting to PBJ in the 2022-2024 period.
2.  **CMS Aberrant Exclusions**: Removal of facilities with quarterly staffing hours outside the plausible range (0-12 HPRD).
3.  **Missing Data Exclusions**: Removal of facilities with fewer than 11 reported quarters or missing valid FIPS codes.
4.  **Outlier Exclusions**: Removal of facility-year observations meeting the |z| > 4 criteria for contract ratios or total hours.
5.  **Final Analytic Sample**: The final number of facilities and counties included in the longitudinal trend analysis.
