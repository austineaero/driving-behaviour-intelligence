"""
Load and clean GPS/IMU data from Oxford RobotCar tiny sample.
"""
from pathlib import Path
import pandas as pd

def load_gps(gps_path):
    """
    Load GPS CSV, use Oxford headers, parse 'timestamp' col to datetime.
    """
    df = pd.read_csv(gps_path)
    print("GPS columns found:", df.columns.tolist())
    # Oxford's GPS headers typically include: ['northing', 'easting', 'zone', 'latitude', 'longitude', 'altitude', 'timestamp']
    if "timestamp" not in df.columns:
        raise ValueError(f"timestamp column not found in GPS data columns: {df.columns}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns", errors="coerce")
    # Use latitude, longitude, altitude; drop others if you want
    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "altitude": "alt"
    })
    df = df.dropna(subset=["lat", "lon", "alt", "timestamp"])
    return df[["timestamp", "lat", "lon", "alt"]]

def load_ins(ins_path):
    """
    Load INS CSV, use Oxford headers, parse 'timestamp' col to datetime.
    Use velocity columns and orientation (roll, pitch, yaw).
    """
    df = pd.read_csv(ins_path)
    print("INS columns found:", df.columns.tolist())
    if "timestamp" not in df.columns:
        raise ValueError(f"timestamp column not found in INS data columns: {df.columns}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns", errors="coerce")
    cols_needed = [
        "timestamp", "velocity_north", "velocity_east", "velocity_down",
        "roll", "pitch", "yaw"
    ]
    for c in cols_needed:
        if c not in df.columns:
            raise ValueError(f"Column {c} not found in INS file {ins_path}")
    df = df[cols_needed].dropna()
    return df

def merge_sensors(gps_df, imu_df):
    """
    Merge GPS and IMU on nearest timestamp (left-join GPS, 10ms tolerance).

    Returns
    -------
    pd.DataFrame
    """
    gps_df = gps_df.sort_values("timestamp").copy()
    imu_df = imu_df.sort_values("timestamp").copy()
    merged = pd.merge_asof(
        gps_df, imu_df,
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("10ms")
    )
    merged = merged.dropna()
    return merged