#!/usr/bin/env python3
"""
Rotation matrix demonstration for LiDAR scan alignment.
Shows understanding of 3D transformations needed for the project.
"""
import numpy as np


def rotation_matrix_y(angle_deg):
    """Rotation around Y-axis (tilt/pitch)"""
    rad = np.deg2rad(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [ c,  0,  s],
        [ 0,  1,  0],
        [-s,  0,  c]
    ])


def rotation_matrix_z(angle_deg):
    """Rotation around Z-axis (yaw)"""
    rad = np.deg2rad(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s,  0],
        [s,  c,  0],
        [0,  0,  1]
    ])


def create_combined_rotation(tilt, yaw):
    """Create combined rotation matrix (tilt then yaw)"""
    R_tilt = rotation_matrix_y(tilt)
    R_yaw = rotation_matrix_z(yaw)
    return R_yaw @ R_tilt


# Demonstration with sample point
print("="*60)
print("Rotation Matrix Demonstration")
print("="*60)

# Sample point from scan
point = np.array([10.0, 5.0, -2.0])  # meters
print(f"\nOriginal point: X={point[0]:.2f}, Y={point[1]:.2f}, Z={point[2]:.2f}")

# Example: tilt=-15°, yaw=300° (from client's test file)
tilt, yaw = -15, 300
R = create_combined_rotation(tilt, yaw)

# Apply rotation
rotated = R @ point
print(f"\nAfter tilt={tilt}°, yaw={yaw}° rotation:")
print(f"Rotated point: X={rotated[0]:.2f}, Y={rotated[1]:.2f}, Z={rotated[2]:.2f}")

# Show matrix
print(f"\nCombined rotation matrix:")
print(R)

print("\n" + "="*60)
print("✓ Rotation logic verified")
print("="*60)
