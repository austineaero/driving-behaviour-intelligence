"""
Download Oxford Radar RobotCar Tiny Sample dataset (GPS/IMU) and unzip it.
Also auto-detect the traversal folder and print the paths to gps/ins csvs.
"""
import os
import subprocess
from pathlib import Path

def download_data(data_dir="data/raw"):
    """
    Download and unzip the Oxford Radar RobotCar tiny-sample dataset (≈200MB).

    Returns
    -------
    str: Path to the extracted folder containing traversal(s)
    """
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    zip_path = data_dir / "oxford_radar_robotcar_tiny.zip"
    gdrive_id = "1C5b2w1DMpSFlAkyVah8Om5IdokJrlcgs"

    # Download zip
    if not zip_path.exists():
        try:
            subprocess.run([
                "gdown", "--id", gdrive_id, "-O", str(zip_path)
            ], check=True)
        except Exception as e:
            raise RuntimeError(f"gdown download failed: {e}")

    # Unzip to 'tiny_sample'
    extract_root = data_dir / "tiny_sample"
    if not extract_root.exists():
        import zipfile
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_root)
    return str(extract_root)

def get_traversal_root(extract_root):
    """
    Returns the path to the first traversal in the dataset, e.g.,
    data/raw/tiny_sample/<traversal_name>
    """
    extract_root = Path(extract_root)
    for entry in extract_root.iterdir():
        if entry.is_dir():
            return entry
    raise FileNotFoundError(f"No traversal folder found in {extract_root}")

if __name__ == "__main__":
    extract_root = download_data()
    traversal_root = get_traversal_root(extract_root)
    gps_path = traversal_root / "gps" / "gps.csv"
    imu_path = traversal_root / "ins" / "ins.csv"
    print(f"GPS path: {gps_path}")
    print(f"IMU path: {imu_path}")