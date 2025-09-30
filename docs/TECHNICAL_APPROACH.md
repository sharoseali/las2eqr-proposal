# Technical Approach - LAS to Equirectangular Depth Map

## Problem Analysis

We own Livox Avia LiDAR scans from a fixed sensor position, with each scan captured at different tilt and yaw angles. The goal is to merge these into a single 360° equirectangular depth map.

### Key Challenges:
1. **Rotation alignment**: Different tilt/yaw per scan requires 3D rotation matrices
2. **Overlap handling**: Multiple scans may capture the same area (need nearest-return logic)
3. **Spherical projection**: Converting 3D Cartesian to 2D equirectangular
4. **Gap filling**: Inpainting small holes in the final depth map

---

## Detailed Methodology

### Phase 1: LAS File Loading

**Library**: `laspy 2.x`
```python
las = laspy.read(filepath)
# laspy automatically applies scale/offset from header
x, y, z = las.x, las.y, las.z
points = np.column_stack([x, y, z])

# Technical Approach

## Understanding the Problem

Your Livox Avia scans are taken from one position but at different tilt/yaw angles. I need to rotate each scan back to a common reference frame, merge them (keeping the closest return when they overlap), then project everything onto a 360° equirectangular depth image.

## My Approach

### 1. Loading & Parsing (~30 min)

I'll use `laspy` to read the files. The key here is that laspy v2 automatically applies the scale/offset from the LAS header, so I get real-world coordinates in metres right away.

For the filename parsing, a simple regex will extract the tilt and yaw:
```python
pattern = r'_tilt(-?\d+)_yaw(\d+)\.las'
```

One thing I need to verify early: whether your scanner position is at the point cloud centroid, or if there's a known offset I should use. I'll center everything at (0,0,0) to make the math cleaner.

### 2. Rotation Logic (~2-3 hours)

This is the critical part. Each scan needs two rotations:
- **Tilt** (pitch around Y-axis)
- **Yaw** (rotation around Z-axis)

The standard convention is to apply tilt first, then yaw: `R = R_yaw @ R_tilt`

But here's the thing - I've learned that different LiDAR systems use different conventions. So after implementing the standard approach, if the merged cloud doesn't look right, I'll test:
- Opposite rotation order (yaw then tilt)
- Negated angles
- Tilt around X-axis instead of Y-axis

The test data will make it obvious if I got it wrong - misaligned scans will show gaps or double-walls.

### 3. Merging Strategy (~1 hour)

Once all scans are rotated to the same frame, I need to handle overlaps. The spec says "nearest return", which means when multiple points project to the same pixel, keep the one closest to the scanner.

I'll use NumPy's `minimum.at()` for this - it's way faster than looping:
```python
np.minimum.at(depth_map.ravel(), pixel_indices, radial_distances)
```

This handles both overlapping scans AND multiple returns within a single scan automatically.

### 4. Projection to Equirectangular (~2-3 hours)

This is straightforward math:
1. Convert each point from Cartesian (x,y,z) to spherical (azimuth, elevation, range)
2. Map azimuth [0°,360°] linearly to image width
3. Map elevation [-90°,+90°] linearly to image height

The tricky part is getting the conventions right:
- Which direction is azimuth=0°? (I'm assuming +X axis)
- Is elevation measured from XY plane or from +Z?
- Should the image top be +90° or -90°?

I'll verify this by checking if a point directly in front of the scanner appears where expected in the output image.

### 5. Inpainting (~1 hour)

The 3×3 median inpainting is simple with scipy:
- For each NaN pixel, look at the 3×3 neighborhood
- If there are ≥5 valid neighbors, replace with their median
- Otherwise leave it NaN

Two passes should be enough to fill most small gaps. I won't go crazy with more passes since that can start creating artifacts.

## What Could Go Wrong

**Most likely issue**: Getting the rotation convention wrong. This is why I'm outputting the M1 merged point cloud first - you can open it in CloudCompare and immediately see if scans are aligned correctly.

**Second most likely**: Coordinate system assumptions. If I assume the wrong azimuth zero-point or elevation direction, the depth map will be rotated or flipped. Easy to fix once identified.

**Performance**: With 20 files × 900K points = ~18M points, this should process in under a minute on decent hardware. If it's slower, I'll profile and optimize.

## Verification Plan

**M1**: Open the merged .las in CloudCompare. All scans should be aligned with no gaps or double-surfaces. If not, I'll debug the rotation logic.

**M2**: 
1. Check the preview PNG - depth data should be in the expected regions (horizontal bands for your tilt=-15° scans)
2. Verify statistics: coverage should be 60-80% with 20+ scans, depth values should be reasonable (not negative, not absurdly large)
3. If you provide an equirectangular photo from the same location, I can overlay them to verify alignment

## Timeline

- M1 (rotation & merge): 2-3 days
- M2 (projection & inpainting): 3-4 days after M1 approval

Most of the time is testing and validation, not writing code.

---
