
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.stats import pearsonr, chi2_contingency


def describe_df(df):
    
    """
    Toma un DataFrame y devuelve un resumen transpuesto de cada columna con información:
    - Tipo de dato.
    - Porcentaje de valores nulos.
    - Número de valores únicos.
    - Porcentaje de cardinalidad. 

    Argumentos:
    DataFrame que contiene los datos a describir.

    Return:
    DataFrame transpuesto con 'Column' como índice y números redondeados a 2 decimales.
    """


    
    description = pd.DataFrame({
        'Column': df.columns,
        'Data_Type': [df[col].dtype for col in df.columns],
        'Null (%)': [df[col].isnull().mean() * 100 for col in df.columns],
        'Unique_Values': [df[col].nunique() for col in df.columns],
        'Cardin (%)': [(df[col].nunique() / len(df)) * 100 for col in df.columns]
    })
    
    # Establecer 'Column' como índice
    description.set_index('Column', inplace=True)
    
    # Redondear valores numéricos a 2 decimales
    description = description.round(2)
    
    # Transponer el DataFrame
    return description.T  


def tipifica_variables(df, umbral_categoria, umbral_continua):
  """
  Tipifica las variables de un DataFrame.

  Argumentos:
    df: DataFrame a analizar.
    umbral_categoria: Umbral máximo de cardinalidad para considerar una variable categórica.
    umbral_continua: Umbral mínimo de porcentaje de cardinalidad respecto al total de filas para considerar una variable numérica discreta.

  Returns:
    DataFrame con las columnas 'nombre_variable' y 'tipo_sugerido'.
  """

  tipos = []
  for col in df.columns:
    cardinalidad = df[col].nunique()
    total_filas = df.shape[0]
    porcentaje_cardinalidad = cardinalidad / total_filas

    if cardinalidad == 2:
      tipo = "Binaria"
    elif cardinalidad < umbral_categoria:
      tipo = "Categórica"
    else:
      if porcentaje_cardinalidad >= umbral_continua:
        tipo = "Numérica Continua"
      else:
        tipo = "Numérica Discreta"

    tipos.append(tipo)

  # Crear DataFrame con 'nombre_variable' como índice y un título
  resultado = pd.DataFrame({'tipo_sugerido': tipos})
  resultado.index = df.columns
  resultado.index.name = 'nombre_variable'  # Asigna un nombre al índice

  return resultado

def get_features_num_regression(df, target_col, umbral_corr, pvalue=None):
    """
    Selecciona columnas numéricas con alta correlación con el target para regresión.

    :param df: pd.DataFrame - DataFrame de entrada.
    :param target_col: str - Columna objetivo.
    :param umbral_corr: float - Umbral mínimo de correlación en valor absoluto.
    :param pvalue: float - Valor p para la significancia estadística (opcional).
    :return: list - Lista de nombres de columnas que cumplen los criterios.
    """
    # Validaciones de entrada
    if not isinstance(df, pd.DataFrame):
        print("❌ El argumento 'df' debe ser un DataFrame.")
        return None

    if target_col not in df.columns:
        print(f"❌ La columna objetivo '{target_col}' no está en el DataFrame.")
        return None

    if not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"❌ La columna objetivo '{target_col}' debe ser numérica y continua.")
        return None

    if not (0 <= umbral_corr <= 1):
        print("❌ El argumento 'umbral_corr' debe estar entre 0 y 1.")
        return None

    if pvalue is not None and not (0 <= pvalue <= 1):
        print("❌ El argumento 'pvalue' debe estar entre 0 y 1 o ser None.")
        return None

    # Selección de columnas numéricas
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if target_col in num_cols:
        num_cols.remove(target_col)

    if not num_cols:
        print("⚠️ No se encontraron columnas numéricas en el DataFrame aparte de la columna objetivo.")
        return []

    seleccionadas = []

    for col in num_cols:
        try:
            correlacion = df[[col, target_col]].dropna()
            corr, p = pearsonr(correlacion[col], correlacion[target_col])
            if abs(corr) >= umbral_corr:
                if pvalue is None or p <= (1 - pvalue):
                    seleccionadas.append(col)
        except Exception as e:
            print(f"⚠️ Error al calcular la correlación para la columna '{col}': {e}")

    if not seleccionadas:
        print("⚠️ No se encontraron columnas que cumplan con los criterios especificados.")
        return []

    print(f"✅ Columnas seleccionadas: {seleccionadas}")
    return seleccionadas


def plot_features_num_regression(df, target_col="", columns=[], umbral_corr=0, pvalue=None):
    """
    Genera pairplots para las columnas numéricas seleccionadas en base a su correlación con una columna objetivo.

    :param df: pd.DataFrame - DataFrame de entrada
    :param target_col: str - Columna objetivo
    :param columns: list - Lista de columnas a considerar
    :param umbral_corr: float - Umbral mínimo de correlación en valor absoluto
    :param pvalue: float - Valor p para la significancia estadística (opcional)
    :return: list - Lista de columnas seleccionadas
    """
    # Validaciones de entrada
    if not isinstance(df, pd.DataFrame):
        print("❌ El argumento 'df' debe ser un DataFrame.")
        return None

    if target_col not in df.columns:
        print(f"❌ La columna objetivo '{target_col}' no está en el DataFrame.")
        return None

    if not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"❌ La columna objetivo '{target_col}' debe ser numérica y continua.")
        return None

    if not (0 <= umbral_corr <= 1):
        print("❌ El argumento 'umbral_corr' debe estar entre 0 y 1.")
        return None

    if pvalue is not None and not (0 <= pvalue <= 1):
        print("❌ El argumento 'pvalue' debe estar entre 0 y 1 o ser None.")
        return None

    # Si la lista de columnas está vacía, seleccionamos todas las numéricas menos la columna objetivo
    if not columns:
        columns = df.select_dtypes(include=['number']).columns.tolist()
        if target_col in columns:
            columns.remove(target_col)

    # Validar columnas
    if not all(col in df.columns for col in columns):
        print("❌ Algunas columnas especificadas no están en el DataFrame.")
        return None

    if not all(pd.api.types.is_numeric_dtype(df[col]) for col in columns):
        print("❌ Todas las columnas seleccionadas deben ser numéricas.")
        return None

    seleccionadas = []

    for col in columns:
        try:
            correlacion = df[[col, target_col]].dropna()
            corr, p = pearsonr(correlacion[col], correlacion[target_col])
            if abs(corr) >= umbral_corr:
                if pvalue is None or p <= (1 - pvalue):
                    seleccionadas.append(col)
        except Exception as e:
            print(f"⚠️ Error al calcular la correlación para la columna '{col}': {e}")

    if not seleccionadas:
        print("⚠️ No se encontraron columnas que cumplan con los criterios especificados.")
        return []

    # Generar pairplots
    max_cols_per_plot = 5
    print(f"✅ Columnas seleccionadas para pairplot: {seleccionadas}")
    for i in range(0, len(seleccionadas), max_cols_per_plot - 1):
        subset = seleccionadas[i:i + max_cols_per_plot - 1] + [target_col]
        try:
            sns.pairplot(df[subset].dropna())
            plt.show()
        except Exception as e:
            print(f"⚠️ Error al generar el pairplot para el subconjunto {subset}: {e}")

    return seleccionadas

def get_features_cat_regression(df, target_col, pvalue=0.05):
    """
    Selecciona columnas categóricas relacionadas con la columna objetivo para regresión.

    :param df: pd.DataFrame - DataFrame de entrada.
    :param target_col: str - Columna objetivo.
    :param pvalue: float - Valor p para la significancia estadística (opcional).
    :return: list - Lista de nombres de columnas que cumplen los criterios.
    """
    # Validaciones de entrada
    if not isinstance(df, pd.DataFrame):
        print("❌ El argumento 'df' debe ser un DataFrame.")
        return None

    if target_col not in df.columns:
        print(f"❌ La columna objetivo '{target_col}' no está en el DataFrame.")
        return None

    if not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"❌ La columna objetivo '{target_col}' debe ser numérica y continua.")
        return None

    if pvalue is not None and not (0 <= pvalue <= 1):
        print("❌ El argumento 'pvalue' debe estar entre 0 y 1 o ser None.")
        return None

    # Selección de columnas categóricas
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if not cat_cols:
        print("⚠️ No se encontraron columnas categóricas en el DataFrame.")
        return []

    seleccionadas = []

    for col in cat_cols:
        try:
            tabla_contingencia = pd.crosstab(df[col], df[target_col])
            _, p, _, _ = chi2_contingency(tabla_contingencia)
            if p <= pvalue:
                seleccionadas.append(col)
        except Exception as e:
            print(f"⚠️ Error al analizar la relación para la columna '{col}': {e}")

    if not seleccionadas:
        print("⚠️ No se encontraron columnas que cumplan con los criterios especificados.")
        return []

    print(f"✅ Columnas seleccionadas: {seleccionadas}")
    return seleccionadas

def plot_features_cat_regression(df, target_col="", columns=[], pvalue=0.05, with_individual_plot=False):
    """
    Genera histogramas agrupados de características categóricas en base a su relación con la columna objetivo.

    :param df: pd.DataFrame - DataFrame de entrada.
    :param target_col: str - Columna objetivo.
    :param columns: list - Lista de columnas categóricas a considerar.
    :param pvalue: float - Valor p para la significancia estadística (opcional).
    :param with_individual_plot: bool - Si se deben mostrar histogramas individuales.
    :return: list - Lista de columnas seleccionadas.
    """
    # Validaciones de entrada
    if not isinstance(df, pd.DataFrame):
        print("❌ El argumento 'df' debe ser un DataFrame.")
        return None

    if target_col not in df.columns:
        print(f"❌ La columna objetivo '{target_col}' no está en el DataFrame.")
        return None

    seleccionadas = get_features_cat_regression(df, target_col, pvalue)

    if with_individual_plot:
        for col in seleccionadas:
            sns.histplot(data=df, x=target_col, hue=col, kde=True)
            plt.show()

    return seleccionadas
