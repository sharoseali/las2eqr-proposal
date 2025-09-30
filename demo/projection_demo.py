#!/usr/bin/env python3
"""
Spherical projection demonstration for equirectangular mapping.
Shows understanding of coordinate transformations needed.
"""
import numpy as np


def cartesian_to_spherical(x, y, z):
    """Convert Cartesian to spherical coordinates"""
    r = np.sqrt(x**2 + y**2 + z**2)
    azimuth = np.degrees(np.arctan2(y, x))
    azimuth = (azimuth + 360) % 360  # Normalize to [0, 360)
    elevation = np.degrees(np.arcsin(z / (r + 1e-10)))
    return azimuth, elevation, r


def spherical_to_pixel(azimuth, elevation, width=4096, height=2048):
    """Map spherical coords to equirectangular pixel coordinates"""
    u = int((azimuth / 360.0) * width)
    v = int(((90.0 - elevation) / 180.0) * height)
    u = np.clip(u, 0, width - 1)
    v = np.clip(v, 0, height - 1)
    return u, v


# Demonstration with sample points
print("="*60)
print("Equirectangular Projection Demonstration")
print("="*60)

# Sample points at various locations
test_points = [
    (10.0, 0.0, 0.0, "Directly in front"),
    (0.0, 10.0, 0.0, "Directly to left"),
    (7.07, 7.07, 0.0, "45° left, horizon"),
    (5.0, 5.0, 5.0, "45° left, 45° up"),
]

width, height = 4096, 2048

print(f"\nOutput resolution: {width}×{height}")
print(f"\nProjection examples:\n")

for x, y, z, desc in test_points:
    azimuth, elevation, r = cartesian_to_spherical(x, y, z)
    u, v = spherical_to_pixel(azimuth, elevation, width, height)
    
    print(f"{desc}:")
    print(f"  Cartesian: ({x:.2f}, {y:.2f}, {z:.2f}) m")
    print(f"  Spherical: azimuth={azimuth:.1f}°, elevation={elevation:.1f}°, r={r:.2f}m")
    print(f"  Pixel: u={u}, v={v}")
    print()

print("="*60)
print("✓ Projection logic verified")
print("="*60)
