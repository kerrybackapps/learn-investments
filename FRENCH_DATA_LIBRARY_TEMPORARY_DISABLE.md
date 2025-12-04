# Temporary Disable of Ken French Data Library Access

**Date:** 2025-12-04
**Reason:** Ken French Data Library (mba.tuck.dartmouth.edu) is returning 401 Unauthorized errors, preventing the app from starting

## Problem

The app was failing to start because it was attempting to fetch data from Ken French's Data Library during module initialization. The library is currently returning HTTP 401 errors indicating access is denied.

## Changes Made

### 1. Core Data Import Files (3 files)

These files were modified to wrap data fetches in try-except blocks, setting variables to `None` if the fetch fails:

- **`pages/data/ff_monthly.py`**
  - Variables: `ff3`, `ff5`, `Mom`, `ST_Rev`, `LT_Rev`, `ff48`
  - All wrapped in try-except, set to None on failure

- **`pages/data/ff_annual.py`**
  - Variable: `ff3_annual`
  - Wrapped in try-except, set to None on failure

- **`pages/data/ff_daily.py`**
  - Variable: `ff3_daily`
  - Wrapped in try-except, set to None on failure

### 2. Utility Module (1 new file)

- **`pages/data/data_unavailable.py`** (NEW FILE)
  - `create_unavailable_message_fig()`: Creates a Plotly figure displaying "Access to Ken French's Data Library is temporarily unavailable."
  - `create_unavailable_table()`: Returns a placeholder table for unavailable data

### 3. Page Implementation Files (18 files)

All files that import French data were updated to:
1. Import data variables directly (not aliased)
2. Add imports for `create_unavailable_message_fig` and `create_unavailable_table`
3. Check if data is None after imports
4. Return unavailable messages in the main `figtbl()` function if data is None

#### Files Modified:

**Borrowing & Saving:**
- `pages/borrowing_saving/inflation_figtbl.py`

**Performance Evaluation:**
- `pages/performance_evaluation/user_returns_figtbl.py`
- `pages/performance_evaluation/funds_figtbl.py`

**Risk Analysis:**
- `pages/risk/best_worst_figtbl.py`
- `pages/risk/frequencies_figtbl.py`
- `pages/risk/geometric_figtbl.py`
- `pages/risk/returns_figtbl.py`
- `pages/risk/volatilities_figtbl.py`

**CAPM Analysis:**
- `pages/capm/alphas_betas_figtbl.py`
- `pages/capm/capm_costequity_figtbl.py`
- `pages/capm/sml_industries_figtbl.py`
- `pages/capm/two_way_capm_figtbl.py`

**Factor Investing:**
- `pages/factor_investing/ff_costequity_figtbl.py`
- `pages/factor_investing/quintiles_figtbl.py`
- `pages/factor_investing/ff_industries_figtbl.py`
- `pages/factor_investing/two_way_sorts_figtbl.py`
- `pages/factor_investing/ff_characteristics_figtbl.py`

## How to Revert These Changes

When Ken French's Data Library becomes accessible again, follow these steps to restore full functionality:

### Step 1: Revert Core Data Files

**In `pages/data/ff_monthly.py`:**
```python
# REMOVE the try-except wrapper and TEMPORARY comment
# Change FROM:
# TEMPORARY: Ken French Data Library access is currently unavailable
try:
    ff3 = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[0]/100
    ff5 = pdr('F-F_Research_Data_5_Factors_2x3','famafrench', start=1900)[0]/100
    Mom = pdr('F-F_Momentum_Factor','famafrench', start=1900)[0]/100
    ST_Rev = pdr('F-F_ST_Reversal_Factor','famafrench', start=1900)[0]/100
    LT_Rev = pdr('F-F_LT_Reversal_Factor','famafrench', start=1900)[0]/100
    ff48 = pdr("48_Industry_Portfolios", "famafrench", start=1900)[0]/100
except Exception as e:
    print(f"Warning: Unable to access Ken French Data Library: {e}")
    ff3 = None
    ff5 = None
    Mom = None
    ST_Rev = None
    LT_Rev = None
    ff48 = None

# Change TO:
ff3 = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[0]/100
ff5 = pdr('F-F_Research_Data_5_Factors_2x3','famafrench', start=1900)[0]/100
Mom = pdr('F-F_Momentum_Factor','famafrench', start=1900)[0]/100
ST_Rev = pdr('F-F_ST_Reversal_Factor','famafrench', start=1900)[0]/100
LT_Rev = pdr('F-F_LT_Reversal_Factor','famafrench', start=1900)[0]/100
ff48 = pdr("48_Industry_Portfolios", "famafrench", start=1900)[0]/100
```

**In `pages/data/ff_annual.py`:**
```python
# REMOVE the try-except wrapper and TEMPORARY comment
# Change FROM:
# TEMPORARY: Ken French Data Library access is currently unavailable
try:
    ff3_annual = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[1]/100
except Exception as e:
    print(f"Warning: Unable to access Ken French Data Library: {e}")
    ff3_annual = None

# Change TO:
ff3_annual = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[1]/100
```

**In `pages/data/ff_daily.py`:**
```python
# REMOVE the try-except wrapper and TEMPORARY comment
# Change FROM:
# TEMPORARY: Ken French Data Library access is currently unavailable
try:
    ff3_daily = pdr('F-F_Research_Data_Factors_daily','famafrench', start=1900)[0]/100
except Exception as e:
    print(f"Warning: Unable to access Ken French Data Library: {e}")
    ff3_daily = None

# Change TO:
ff3_daily = pdr('F-F_Research_Data_Factors_daily','famafrench', start=1900)[0]/100
```

### Step 2: Revert Page Implementation Files

For each of the 18 modified page files, you need to:

1. **Remove the import** of `data_unavailable`:
   ```python
   # REMOVE this line:
   from pages.data.data_unavailable import create_unavailable_message_fig, create_unavailable_table
   ```

2. **Remove the TEMPORARY comment** and availability check at module level

3. **Remove the early return check** in the `figtbl()` function

**Example for `pages/borrowing_saving/inflation_figtbl.py`:**

```python
# Change FROM:
from pages.data.ff_annual import ff3_annual
from pages.data.data_unavailable import create_unavailable_message_fig

# TEMPORARY: Check if French data is available
if ff3_annual is not None:
    mkt = ff3_annual["Mkt-RF"] + ff3_annual.RF
    # ... rest of data processing
else:
    df = None

def figtbl(dates):
    if df is None:
        fig = create_unavailable_message_fig()
        return fig, fig, "N/A", "N/A", "N/A"
    # ... rest of function

# Change TO:
from pages.data.ff_annual import ff3_annual

mkt = ff3_annual["Mkt-RF"] + ff3_annual.RF
# ... rest of data processing

def figtbl(dates):
    # ... rest of function (no early return check)
```

### Step 3: Delete Utility File (Optional)

Once all references are removed, you can delete:
- `pages/data/data_unavailable.py`

### Step 4: Test

After reverting:
1. Restart the application
2. Test pages in each category:
   - Borrowing & Saving → Inflation page
   - Risk Analysis → Returns, Volatilities pages
   - CAPM → Alphas & Betas page
   - Factor Investing → Any factor page
3. Verify data loads correctly and figures display properly

## Quick Checklist for Reverting

- [ ] Revert `pages/data/ff_monthly.py`
- [ ] Revert `pages/data/ff_annual.py`
- [ ] Revert `pages/data/ff_daily.py`
- [ ] Revert all 18 page implementation files (remove imports, checks, and early returns)
- [ ] Delete `pages/data/data_unavailable.py` (optional)
- [ ] Test application startup
- [ ] Test pages that use French data
- [ ] Delete this documentation file

## Notes

- All changes are marked with "TEMPORARY" comments for easy identification
- The changes are backward compatible - if French data becomes available, the app will work normally
- When unavailable, pages display: "Access to Ken French's Data Library is temporarily unavailable."
- No functionality was removed, only graceful error handling was added

## Search for Changes

To find all temporary changes, search the codebase for:
- `TEMPORARY` (comment marker)
- `create_unavailable_message_fig` (function name)
- `data_unavailable` (module name)
