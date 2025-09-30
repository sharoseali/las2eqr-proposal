# Setup

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/las2eqr-proposal.git
cd las2eqr-proposal

# Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Demos

### Test LAS file loading

Download one of the test files from your Google Drive link, then:

```bash
python demo/verify_las.py
```

You should see the point count and header info printed out.

### Test rotation logic

```bash
python demo/rotation_demo.py
```

This shows how I'll rotate each scan based on its tilt/yaw angles.

### Test projection

```bash
python demo/projection_demo.py
```

This demonstrates the spherical-to-equirectangular conversion.

## What's Here

This is a **proposal demo** showing my approach. The complete working system will be delivered after contract award with:
- Full CLI (`las2eqr.py /path/to/scans --width 4096 --height 2048`)
- All the rotation and merging logic
- Rasterization and inpainting
- Proper error handling and logging

## Dependencies

- Python 3.11+
- laspy 2.5+ (LAS I/O)
- numpy 1.26+ (array operations)
- scipy 1.11+ (inpainting)
- tifffile 2024+ (TIFF output)

That's it. Standard libraries that work cross-platform.

## Questions?

Reach out via Upwork if you want to discuss the approach before awarding the contract.
