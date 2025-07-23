"""
Plotting and route visualisation.
"""
import matplotlib.pyplot as plt
from pathlib import Path

def plot_feature_importance(model, features, out_path):
    """
    Bar plot of feature importances.
    """
    importances = model.feature_importances_
    sorted_idx = importances.argsort()[::-1]
    fi = importances[sorted_idx]
    names = [features[i] for i in sorted_idx]
    plt.figure(figsize=(8, 4))
    plt.bar(range(len(fi)), fi)
    plt.xticks(range(len(fi)), names, rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_route(df, risk_col, out_path):
    """
    Plot lat-lon route colored by risk label.
    """
    cmap = {0: "green", 1: "red"}
    colors = df[risk_col].map(cmap)
    plt.figure(figsize=(6, 6))
    plt.scatter(df["lon"], df["lat"], c=colors, s=8)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Route colored by predicted risk")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()