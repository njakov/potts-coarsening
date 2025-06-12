# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 18:07:15 2025

@author: ninaj
"""

import glob
import re
from PIL import Image
import matplotlib.pyplot as plt
import io

image_folder = 'snapshots'
output_gif = 'ordering_process.gif'
n_images = 400

conf_labels = range(1, n_images+1)

image_files = glob.glob(f'{image_folder}/lattice_step_*.png')

# Sort by the numeric part extracted from filename
image_files_sorted = sorted(image_files, key=lambda x: int(re.findall(r'\d+', x)[0]))

# Take first n_images after sorting
image_files_sorted = image_files_sorted[:n_images]

assert len(image_files_sorted) == n_images, f"Found {len(image_files)} images, expected {n_images}"

frames = []
for img_path, conf_label in zip(image_files_sorted, conf_labels):
    img = Image.open(img_path).convert('L')  # Convert to grayscale here
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img, cmap='gray')  # Use grayscale colormap in matplotlib
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # Save figure to buffer
    plt.close(fig)
    buf.seek(0)
    frame = Image.open(buf).convert('L')  # Convert saved frame to grayscale
    frames.append(frame)

frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=100,  # milliseconds per frame
    loop=0          # loop forever
)
print(f'GIF saved as {output_gif}')

    
    
