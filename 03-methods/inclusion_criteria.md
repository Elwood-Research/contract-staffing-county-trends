# Inclusion and Exclusion Criteria

## Study Population
The study includes all Medicare and Medicaid-certified nursing facilities in the United States that report data to the Payroll-Based Journal (PBJ) system.

## Inclusion Criteria
1. **Timeframe**: Data must be from January 1, 2022, to December 31, 2024.
2. **Data Availability**: Facilities must have valid reported hours and census for the quarters analyzed.
3. **Geographic Coverage**: Facilities must be located within a US county with a valid FIPS code.

## Exclusion Criteria
1. **Aberrant Staffing (CMS Standard)**: Facilities are excluded if their quarterly aggregate staffing meets any of the following:
    - Total nurse staffing = 0 hours per resident per day.
    - Total nurse staffing > 12 hours per resident per day.
    - Nurse aide staffing > 5.25 hours per resident per day.
2. **Small Sample Counties**: For county-level aggregation, counties with fewer than 3 reporting facilities may be flagged or excluded from specific geospatial analyses to ensure stability of the mean.
3. **Extreme Outliers (Study Specific)**:
    - Observations with |z| > 4 for continuous staffing variables will be removed before aggregation.
    - This rule is applied specifically to:
        - **Total Nursing Hours per Resident Day**: Aggregated daily nursing hours divided by resident census.
        - **Contract Ratio**: The proportion of contract hours relative to total hours.
