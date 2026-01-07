import pandas as pd

# Loading the Excel file
df = pd.read_excel('data/raw/social_media_raw.xlsx') 

# Selecting all text columns
text_cols = df.select_dtypes(include='object').columns

# Creating a dictionary to store mappings
mapping_dict = {}

# Adding code columns and collect mappings
for col in text_cols:
    cat_series = df[col].astype('category')
    df[f'{col}_Code'] = cat_series.cat.codes + 1  # +1 to start codes from 1 instead of -1 for NaN

    # Build mapping dataframe safely
    code_to_label = {
        code + 1: label for code, label in enumerate(cat_series.cat.categories)
    }
    mapping_df = pd.DataFrame(list(code_to_label.items()), columns=[f'{col}_Code', col])
    mapping_dict[col] = mapping_df

# Save the updated data with code columns
df.to_excel('data/processed/social_media_encoded.xlsx', index=False)

# Save the mappings to a separate Excel file (one sheet per column)
with pd.ExcelWriter('data/metadata/encoding_legend.xlsx') as writer:
    for col, map_df in mapping_dict.items():
        map_df.to_excel(writer, sheet_name=col[:31], index=False)  # Sheet names must be ≤ 31 chars

print("Successfully Created Excel Sheets")
