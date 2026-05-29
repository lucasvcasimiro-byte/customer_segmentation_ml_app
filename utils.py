import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns
import math
from sklearn.preprocessing import RobustScaler


def load_data(path):
    return pd.read_csv(path)


def plot_distribution_grid(df, columns):
    """Plots a grid of histograms to see data spread."""
    num_cols = len(columns)
    cols = 4
    rows = math.ceil(num_cols / cols)
    plt.figure(figsize=(12, 3.5 * rows))
    for i, col in enumerate(columns, 1):
        plt.subplot(rows, cols, i)
        sns.histplot(df[col], kde=True)
        plt.title(f'{col}', fontsize=8)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    plt.show()


def plot_boxplot_grid(df, columns):
    """Plots a grid of boxplots to detect outliers."""
    num_cols = len(columns)
    cols = 4
    rows = math.ceil(num_cols / cols)
    plt.figure(figsize=(12, 3.5 * rows))
    for i, col in enumerate(columns, 1):
        plt.subplot(rows, cols, i)
        sns.boxplot(y=df[col])
        plt.title(f'{col}', fontsize=8)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    plt.show()


def plot_correlation_heatmap(df, columns):
    """Generates a clean, masked heatmap."""
    corr = df[columns].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm')
    plt.title("Correlation Heatmap (Numerical Features)")
    plt.show()