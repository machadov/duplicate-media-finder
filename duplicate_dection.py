import argparse
import os
import json
from PIL import Image
import imagehash
import cv2
from tqdm import tqdm
import numpy as np
from collections import defaultdict
from scipy.spatial import distance
from multiprocessing import Pool, cpu_count

def parse_arguments():
    parser = argparse.ArgumentParser(description='Find duplicate images and videos based on content.')
    parser.add_argument('folders', nargs='+', help='Folders to scan for images and videos.')
    parser.add_argument('-t', '--threshold', type=float, default=0.9, help='Similarity threshold (0-1). Default is 0.9.')
    parser.add_argument('-o', '--output', default='output.txt', help='Output file to save the results.')
    parser.add_argument('--no-images', action='store_true', help='Disable image comparison.')
    parser.add_argument('--no-videos', action='store_true', help='Disable video comparison.')
    parser.add_argument('--processes', type=int, default=cpu_count(), help='Number of processes to use. Default is the number of CPU cores.')
    return parser.parse_args()

def get_media_files(folder_paths, extensions):
    media_files = []
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(extensions):
                    media_files.append(os.path.join(root, file))
    return media_files

def generate_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            img_hash = imagehash.phash(img)
            return (image_path, img_hash)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def generate_image_hashes(image_files, processes):
    print("Generating image hashes...")
    hashes = {}
    with Pool(processes=processes) as pool:
        for result in tqdm(pool.imap_unordered(generate_image_hash, image_files), total=len(image_files), desc="Processing images"):
            if result is not None:
                file_path, img_hash = result
                hashes[file_path] = img_hash
    return hashes

def extract_video_hash(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_number = frame_count // 2  # Get the middle frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        if ret:
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            video_hash = imagehash.phash(pil_image)
            return (video_path, video_hash)
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
    return None

def extract_video_hashes(video_files, processes):
    print("Generating video hashes...")
    hashes = {}
    with Pool(processes=processes) as pool:
        for result in tqdm(pool.imap_unordered(extract_video_hash, video_files), total=len(video_files), desc="Processing videos"):
            if result is not None:
                file_path, vid_hash = result
                hashes[file_path] = vid_hash
    return hashes

def hash_to_vector(hash_obj):
    # Convert imagehash object to numpy array
    return np.array(hash_obj.hash).astype(np.float32).flatten()

def group_similar_hashes(hashes, threshold, processes):
    # Group hashes into buckets based on hash value
    hash_buckets = defaultdict(list)
    for file_path, img_hash in hashes.items():
        # Use a portion of the hash as a key (e.g., first 8 bits)
        bucket_key = str(img_hash)[:8]
        hash_buckets[bucket_key].append((file_path, img_hash))
    
    similar_groups = []
    tasks = [(bucket_files, threshold) for bucket_files in hash_buckets.values() if len(bucket_files) > 1]

    with Pool(processes=processes) as pool:
        results = pool.imap_unordered(compare_bucket, tasks)
        for group in results:
            similar_groups.extend(group)
    return similar_groups

def compare_bucket(args):
    bucket_files, threshold = args
    group_results = []
    vectors = [hash_to_vector(h) for _, h in bucket_files]
    file_paths = [fp for fp, _ in bucket_files]
    # Compute pairwise distances
    dists = distance.pdist(vectors, 'hamming')
    dist_matrix = distance.squareform(dists)
    n = len(bucket_files)
    visited = set()
    for i in range(n):
        if i in visited:
            continue
        group = [file_paths[i]]
        for j in range(i+1, n):
            if dist_matrix[i, j] <= (1 - threshold):
                group.append(file_paths[j])
                visited.add(j)
        if len(group) > 1:
            similarity = (1 - dist_matrix[i, j]) * 100
            group_results.append({'files': group, 'similarity': round(similarity, 2)})
    return group_results

def save_results(image_groups, video_groups, output_file):
    results = {}
    if image_groups is not None:
        results['images'] = image_groups
    if video_groups is not None:
        results['videos'] = video_groups
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

def main():
    args = parse_arguments()

    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

    # Initialize result variables
    image_groups = None
    video_groups = None

    # Process images if not disabled
    if not args.no_images:
        print("Scanning for image files...")
        image_files = get_media_files(args.folders, image_extensions)
        if image_files:
            image_hashes = generate_image_hashes(image_files, args.processes)
            print("Grouping similar images...")
            image_groups = group_similar_hashes(image_hashes, args.threshold, args.processes)
        else:
            print("No image files found to process.")
    else:
        print("Image comparison disabled.")

    # Process videos if not disabled
    if not args.no_videos:
        print("Scanning for video files...")
        video_files = get_media_files(args.folders, video_extensions)
        if video_files:
            video_hashes = extract_video_hashes(video_files, args.processes)
            print("Grouping similar videos...")
            video_groups = group_similar_hashes(video_hashes, args.threshold, args.processes)
        else:
            print("No video files found to process.")
    else:
        print("Video comparison disabled.")

    # Save results
    save_results(image_groups, video_groups, args.output)

if __name__ == '__main__':
    main()
