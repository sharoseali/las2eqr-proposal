#!/usr/bin/env python3
"""
Mini verification snippet: Read LAS file and display metadata.
Demonstrates understanding of laspy and client's data format.
"""
import laspy

# Read the LAS file (adjust path as needed)
las_file = laspy.read('scan_20250927_105827_tilt-015_yaw300.las')

# Extract point count
point_count = len(las_file.points)

# Extract header scale and offset
scale = las_file.header.scales
offset = las_file.header.offsets

# Print results
print("="*60)
print("LAS File Analysis: scan_20250927_105827_tilt-015_yaw300.las")
print("="*60)
print(f"\nTotal Point Count: {point_count:,}")
print(f"\nHeader Scale Values:")
print(f"  X scale: {scale[0]}")
print(f"  Y scale: {scale[1]}")
print(f"  Z scale: {scale[2]}")
print(f"\nHeader Offset Values:")
print(f"  X offset: {offset[0]}")
print(f"  Y offset: {offset[1]}")
print(f"  Z offset: {offset[2]}")
print(f"\nCoordinate Ranges (after scale/offset applied):")
print(f"  X: {las_file.x.min():.2f} to {las_file.x.max():.2f} m")
print(f"  Y: {las_file.y.min():.2f} to {las_file.y.max():.2f} m")
print(f"  Z: {las_file.z.min():.2f} to {las_file.z.max():.2f} m")
print("="*60)
