"""
Create driving-behaviour telematics features.
"""
import numpy as np
import pandas as pd
from geopy.distance import geodesic

def haversine_speed(df):
    """
    Compute speed (m/s) between consecutive GPS points using haversine distance.
    """
    shifted = df[["lat", "lon"]].shift()
    merged = df.join(shifted, rsuffix="_prev")
    def pair_dist(row):
        try:
            p1 = (row.lat_prev, row.lon_prev)
            p2 = (row.lat, row.lon)
            if pd.isnull(p1[0]) or pd.isnull(p1[1]):
                return 0.0
            return geodesic(p1, p2).meters
        except:
            return 0.0
    dists = merged.apply(pair_dist, axis=1)
    dt = merged["timestamp"].diff().dt.total_seconds().fillna(1)
    return dists / dt.replace(0, 1)

def engineer_features(df):
    """
    Add telematics features: speed, acceleration from velocity, orientation deltas.
    """
    df = df.copy()
    # Compute planar (horizontal) speed in m/s
    df["speed_mps"] = np.sqrt(df["velocity_north"]**2 + df["velocity_east"]**2)
    df["speed_kph"] = df["speed_mps"] * 3.6
    # Compute horizontal acceleration (m/s^2)
    dt = df["timestamp"].diff().dt.total_seconds().replace(0, 1).fillna(1)
    df["acc_north"] = df["velocity_north"].diff() / dt
    df["acc_east"] = df["velocity_east"].diff() / dt
    df["acc_mag"] = np.sqrt(df["acc_north"]**2 + df["acc_east"]**2)
    # Turning rate (from yaw)
    df["yaw_rate"] = df["yaw"].diff() / dt
    # Harsh events (define thresholds as appropriate)
    df["harsh_brake"] = (df["acc_north"] < -3.5).astype(int)
    df["harsh_accel"] = (df["acc_north"] > 3.5).astype(int)
    df["harsh_turn"] = (np.abs(df["yaw_rate"]) > 0.2).astype(int) # 0.2 rad/s ~ 11 deg/s
    df["speeding"] = (df["speed_kph"] > 80).astype(int)
    df["risky"] = (
        df[["harsh_brake", "harsh_accel", "harsh_turn", "speeding"]].sum(axis=1) > 0
    ).astype(int)
    df = df.fillna(0)
    return df