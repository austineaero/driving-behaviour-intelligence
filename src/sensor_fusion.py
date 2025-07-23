"""
Sensor fusion features: sharp turn detection and heading change using yaw.
"""

import numpy as np
import pandas as pd

def compute_heading(df):
    """
    Use 'yaw' in degrees (from Oxford INS), wrap to [0, 360).
    """
    # Oxford's yaw is in degrees (if not, adjust accordingly)
    heading = df["yaw"] % 360
    heading = heading.fillna(method="bfill").fillna(0)
    return heading

def add_fused_features(df):
    """
    Add heading, heading change, and sharp turn detection.
    Uses 'yaw' for heading; uses 'yaw_rate' for turn events.
    """
    df = df.copy()
    df["heading"] = compute_heading(df)
    # Heading change between points
    df["heading_change"] = df["heading"].diff().abs().fillna(0)
    # Sharp turn: large heading change OR large yaw_rate (from engineer_features)
    df["sharp_turn"] = (
        (df["heading_change"] > 20) | (np.abs(df.get("yaw_rate", 0)) > 0.2)
    ).astype(int)
    return df