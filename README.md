# Duplicate Media Finder

A command-line tool to find and group duplicate images and videos based on content similarity.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Command-Line Options](#command-line-options)
  - [Examples](#examples)
- [How It Works](#how-it-works)
- [Performance Optimizations](#performance-optimizations)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Introduction

**Duplicate Media Finder** is a Python-based command-line utility designed to help you identify duplicate or similar images and videos across one or more folders. Unlike traditional tools that rely on file names or metadata, this tool analyzes the actual content of media files to determine similarity, making it highly effective even when files have been renamed or modified slightly.

## Features

- **Content-Based Comparison**: Compares media files based on their actual content, not just file names or sizes.
- **Supports Images and Videos**: Handles a variety of image and video formats.
- **Recursive Folder Scanning**: Searches through all subfolders in the specified directories.
- **Adjustable Similarity Threshold**: Allows you to specify how similar files must be to be considered duplicates.
- **Disable Media Types**: Optionally disable image or video comparison.
- **Performance Optimizations**: Optimized for large datasets with efficient algorithms and reduced memory usage.
- **Detailed Output**: Generates a JSON file grouping similar files along with their similarity percentages.
- **Progress Indicators**: Provides real-time feedback on the scanning and comparison processes.

## Installation

### Prerequisites

- **Python 3.6 or newer**: Ensure Python is installed on your machine.
- **pip**: Python package manager (usually installed with Python).

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/duplicate-media-finder.git
   cd duplicate-media-finder
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not provided, you can install the packages manually:

   ```bash
   pip install Pillow imagehash opencv-python tqdm scipy
   ```

## Usage

### Basic Usage

Run the script from the command line, specifying one or more folders to scan:

```bash
python duplicate_finder.py /path/to/folder1 /path/to/folder2
```

### Command-Line Options

- **`-t`, `--threshold`**: Set the similarity threshold (0 to 1). Default is `0.9` (90% similarity).

  ```bash
  python duplicate_finder.py /path/to/folder -t 0.95
  ```

- **`-o`, `--output`**: Specify the output file to save the results. Default is `output.txt`.

  ```bash
  python duplicate_finder.py /path/to/folder -o duplicates.json
  ```

- **`--no-images`**: Disable image comparison.

  ```bash
  python duplicate_finder.py /path/to/folder --no-images
  ```

- **`--no-videos`**: Disable video comparison.

  ```bash
  python duplicate_finder.py /path/to/folder --no-videos
  ```

### Examples

#### Example 1: Basic Scan

Scan a single folder with default settings.

```bash
python duplicate_finder.py /Users/username/Pictures
```

#### Example 2: Multiple Folders and Custom Threshold

Scan multiple folders and set a custom similarity threshold of 95%.

```bash
python duplicate_finder.py /path/to/folder1 /path/to/folder2 -t 0.95
```

#### Example 3: Disable Image Comparison

Scan folders but only compare videos.

```bash
python duplicate_finder.py /path/to/folder --no-images
```

#### Example 4: Disable Video Comparison

Scan folders but only compare images.

```bash
python duplicate_finder.py /path/to/folder --no-videos
```

#### Example 5: Specify Output File

Save the results to a specific file.

```bash
python duplicate_finder.py /path/to/folder -o results.json
```

## How It Works

1. **Folder Scanning**: The tool recursively scans the provided folders for media files. Supported image formats include PNG, JPEG, BMP, GIF, and TIFF. Supported video formats include MP4, AVI, MOV, MKV, and FLV.

2. **Hash Generation**:
   - **Images**: Generates perceptual hashes for each image using the `imagehash` library, which is built on top of the `Pillow` library.
   - **Videos**: Extracts the middle frame of each video and generates a perceptual hash for that frame.

3. **Content Comparison**: Compares the hashes of the media files to calculate a similarity score. The similarity is calculated based on the Hamming distance between the hashes.

4. **Performance Optimizations**:
   - **Hash Bucketing**: Files are grouped into buckets based on a portion of their hash values to reduce the number of comparisons.
   - **Efficient Data Structures**: Utilizes dictionaries and NumPy arrays for efficient data storage and computation.
   - **Reduced Memory Usage**: Processes data in a way that minimizes memory consumption, suitable for large datasets.

5. **Grouping Similar Files**: Files with a similarity score equal to or greater than the specified threshold are grouped together.

6. **Output Generation**: The results are saved in a JSON file, grouping similar files and including their similarity percentages.

## Performance Optimizations

- **Reduced Computation Time**: By grouping files into hash buckets and only comparing files within the same bucket, the number of pairwise comparisons is significantly reduced.
- **Memory Efficiency**: Efficient data structures like NumPy arrays and dictionaries are used to minimize memory usage.
- **Scalability**: Optimized to handle large datasets effectively.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of this page to create a copy of the repository on your account.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/duplicate-media-finder.git
   cd duplicate-media-finder
   ```

3. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**

   Implement your changes or new features.

5. **Commit and Push**

   ```bash
   git add .
   git commit -m "Add your commit message here"
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**

   Go to the original repository and create a pull request from your fork.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[Pillow](https://python-pillow.org/)**: Python Imaging Library used for image processing.
- **[ImageHash](https://github.com/JohannesBuchner/imagehash)**: Library used for generating perceptual hashes of images.
- **[OpenCV](https://opencv.org/)**: Used for video processing and frame extraction.
- **[tqdm](https://github.com/tqdm/tqdm)**: Provides progress bars for long-running operations.
- **[NumPy](https://numpy.org/)**: Fundamental package for scientific computing with Python.
- **[SciPy](https://www.scipy.org/)**: Used for efficient distance calculations.

---

Feel free to customize this `README.md` file to suit your specific repository and include any additional information relevant to your project.
