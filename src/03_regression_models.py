import pandas as pd
import statsmodels.api as sm
import numpy as np

def run_ols_regression(df, x_cols, y_col, model_name="Model"):
    """
    Runs an OLS regression model on specific columns and prints a formatted summary.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
        x_cols (list): List of column names for independent variables.
        y_col (str): Column name for the dependent variable.
        model_name (str): Label for the output (e.g., "Engagement Analysis").
    """
    print(f"\n{'='*20} RUNNING: {model_name} {'='*20}")

    # 1. Cleaning Data: select columns and drop NaNs
    try:
        data = df[x_cols + [y_col]].dropna()
    except KeyError as e:
        print(f"Error: Column not found in dataset: {e}")
        return

    # 2. Defining X (Independent) and Y (Dependent)
    X = sm.add_constant(data[x_cols])  # Adds intercept (Constant)
    y = data[y_col]

    # 3. Fit Regression
    model = sm.OLS(y, X).fit()

    # 4. Extract Key Statistics
    n_obs = int(model.nobs)
    r_squared = model.rsquared
    adj_r_squared = model.rsquared_adj
    multiple_r = np.sqrt(r_squared)
    std_error = np.sqrt(model.mse_resid)

    # 5. Extract Coefficients Table
    coef_df = model.summary2().tables[1].reset_index()
    coef_df.rename(columns={
        'index': 'Variable',
        'Coef.': 'Coefficient',
        'Std.Err.': 'Std Error',
        'P>|t|': 'P-Value'
    }, inplace=True)

    # 6. Formatting for Readability
    coef_df['Coefficient'] = coef_df['Coefficient'].round(4)
    coef_df['Std Error'] = coef_df['Std Error'].round(4)
    
    # Custom P-value formatting
    coef_df['P-Value'] = coef_df['P-Value'].apply(lambda p: "< 0.001" if p < 0.001 else f"{p:.4f}")

    # 7. Print Output
    print(f"\n{'='*5} Summary Stats {'='*6}")
    print(f"Multiple R        : {multiple_r:.4f}")
    print(f"R Square          : {r_squared:.4f}")
    print(f"Adjusted R Square : {adj_r_squared:.4f}")
    print(f"Standard Error    : {std_error:.4f}")
    print(f"Observations      : {n_obs}")
    print(f"\n{'='*24} Coefficients Table {'='*24}")
    print(coef_df[['Variable', 'Coefficient', 'Std Error', 'P-Value']].to_string(index=False))
    print("\n")


if __name__ == "__main__":
    file_path = 'data/processed/social_media_encoded.xlsx'

    df = pd.read_excel(file_path)

    # --- MODEL 1: Engagement Analysis ---
    cols_model_1 = [
        'Engaging (Short Videos)_Code', 
        'Engaging (Long Videos)_Code', 
        'Engaging (Stories)_Code', 
        'Engaging (Private Messaging)_Code', 
        'Engaging (Interactive Features)_Code'
    ]
    run_ols_regression(df, x_cols=cols_model_1, y_col='Social Media Use_Code', model_name="Model 1: Engagement Factors")

    # --- MODEL 2: Mental Health Impact ---
    cols_model_2 = [
        'Emotional Impact_Code', 
        'Connected_Code', 
        'Overwhelmed_Code', 
        'Affects Sleep_Code', 
        'Break_Code'
    ]
    run_ols_regression(df, x_cols=cols_model_2, y_col='Social Media Use_Code', model_name="Model 2: Mental Health Impact")

    # --- MODEL 3: Churn/Stoppage Analysis ---
    cols_model_3 = [
        'Reason 1 (Interest)_Code', 
        'Reason 2 (Access)_Code', 
        'Reason 3 (Privacy)_Code', 
        'Reason 4 (Offline Interations)_Code'
    ]
    run_ols_regression(df, x_cols=cols_model_3, y_col='Used Then Stopped_Code', model_name="Model 3: Usage Stoppage Reasons")