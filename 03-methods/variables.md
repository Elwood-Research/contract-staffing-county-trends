# Variable Definitions and Mapping

## Facility and Geographic Identifiers
| PBJ Variable | Human-Readable Label | Type | Description |
|--------------|---------------------|------|-------------|
| PROVNUM | Facility Provider Number | String | Medicare provider number (6 chars) |
| STATE | State | String | Postal abbreviation |
| COUNTY_NAME | County Name | String | Name of the county |
| COUNTY_FIPS | County FIPS Code | String | 3-digit FIPS code for the county |
| WorkDate | Work Date | Date | The specific date for which hours are reported |
| CY_Qtr | Calendar Quarter | String | The calendar year and quarter (e.g., 2022Q1) |

## Nursing Staff Hours
| PBJ Variable | Human-Readable Label | Type | Description |
|--------------|---------------------|------|-------------|
| Hrs_RN | Total Registered Nurse Hours | Numeric | Total paid hours for RNs (Job Code 7) |
| Hrs_RN_ctr | Contract Registered Nurse Hours | Numeric | Contract-based paid hours for RNs |
| Hrs_LPN | Total Licensed Practical Nurse Hours | Numeric | Total paid hours for LPNs (Job Code 9) |
| Hrs_LPN_ctr | Contract Licensed Practical Nurse Hours | Numeric | Contract-based paid hours for LPNs |
| Hrs_CNA | Total Certified Nursing Assistant Hours | Numeric | Total paid hours for CNAs (Job Code 10) |
| Hrs_CNA_ctr | Contract Certified Nursing Assistant Hours | Numeric | Contract-based paid hours for CNAs |

## Derived Analysis Variables
- **Total Nursing Hours**: Sum of `Hrs_RN` (RN), `Hrs_LPN` (LPN), and `Hrs_CNA` (Aide).
- **Total Contract Nursing Hours**: Sum of `Hrs_RN_ctr`, `Hrs_LPN_ctr`, and `Hrs_CNA_ctr`.
- **Contract Ratio**: Calculated as the quotient of total contract nursing hours and total nursing hours:
  $$\text{Contract Ratio} = \frac{\text{Hrs\_RN\_ctr} + \text{Hrs\_LPN\_ctr} + \text{Hrs\_CNA\_ctr}}{\text{Hrs\_RN} + \text{Hrs\_LPN} + \text{Hrs\_CNA}}$$
  This ratio represents the proportion of total direct care nursing hours provided by contract (non-employee) staff.
