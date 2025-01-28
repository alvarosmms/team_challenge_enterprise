# toolbox_ML.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, chi2_contingency

def describe_df(df):
  
    summary = pd.DataFrame({
        "Type": df.dtypes,
        "% Missing": df.isnull().mean() * 100,
        "# Unique": df.nunique(),
        "% Cardinality": (df.nunique() / len(df)) * 100
    })
    return summary

def tipifica_variables(df, umbral_categoria, umbral_continua):
    
    result = []
    for col in df.columns:
        cardinality = df[col].nunique()
        cardinality_percentage = cardinality / len(df)

        if cardinality == 2:
            tipo = "Binaria"
        elif cardinality < umbral_categoria:
            tipo = "Categórica"
        elif cardinality_percentage >= umbral_continua:
            tipo = "Numerica Continua"
        else:
            tipo = "Numerica Discreta"

        result.append({"nombre_variable": col, "tipo_sugerido": tipo})

    return pd.DataFrame(result)

def get_features_num_regression(df, target_col, umbral_corr, pvalue=None):
    
    if target_col not in df.columns or not np.issubdtype(df[target_col].dtype, np.number):
        print("Target column must be numerical and exist in DataFrame.")
        return None

    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    numerical_cols.remove(target_col)

    selected_features = []

    for col in numerical_cols:
        corr, p = pearsonr(df[target_col], df[col])
        if abs(corr) > umbral_corr and (pvalue is None or p < pvalue):
            selected_features.append(col)

    return selected_features

def plot_features_num_regression(df, target_col="", columns=[], umbral_corr=0, pvalue=None):
    
    if not target_col or target_col not in df.columns or not np.issubdtype(df[target_col].dtype, np.number):
        print("Target column must be numerical and exist in DataFrame.")
        return None

    if not columns:
        columns = df.select_dtypes(include=np.number).columns.tolist()

    columns = [col for col in columns if col != target_col]

    filtered_columns = []
    for col in columns:
        corr, p = pearsonr(df[target_col], df[col])
        if abs(corr) > umbral_corr and (pvalue is None or p < pvalue):
            filtered_columns.append(col)

    for i in range(0, len(filtered_columns), 5):
        subset = filtered_columns[i:i + 5]
        sns.pairplot(df, vars=[target_col] + subset)
        plt.show()

    return filtered_columns

def get_features_cat_regression(df, target_col, pvalue=0.05):
   
    if target_col not in df.columns or not np.issubdtype(df[target_col].dtype, np.number):
        print("Target column must be numerical and exist in DataFrame.")
        return None

    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    significant_features = []
    for col in categorical_cols:
        contingency = pd.crosstab(df[col], df[target_col])
        _, p, _, _ = chi2_contingency(contingency)
        if p < pvalue:
            significant_features.append(col)

    return significant_features

def plot_features_cat_regression(df, target_col="", columns=[], pvalue=0.05, with_individual_plot=False):
  
    if not target_col or target_col not in df.columns or not np.issubdtype(df[target_col].dtype, np.number):
        print("Target column must be numerical and exist in DataFrame.")
        return None

    if not columns:
        columns = df.select_dtypes(include="object").columns.tolist()

    significant_columns = []
    for col in columns:
        contingency = pd.crosstab(df[col], df[target_col])
        _, p, _, _ = chi2_contingency(contingency)
        if p < pvalue:
            significant_columns.append(col)

    if with_individual_plot:
        for col in significant_columns:
            sns.histplot(data=df, x=target_col, hue=col, kde=True)
            plt.show()

    return significant_columns