#!/usr/bin/env python3
"""
Setup example images for testing Immerge
This script creates simple test images with different colors and patterns
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path


def create_test_images(output_dir: str = "test_images", num_images: int = 5):
    """Create test images with different colors and patterns"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
    ]
    
    patterns = ['solid', 'gradient', 'circles', 'stripes']
    
    for i in range(num_images):
        img = Image.new('RGB', (512, 512), color='white')
        draw = ImageDraw.Draw(img)
        
        color = colors[i % len(colors)]
        pattern = patterns[i % len(patterns)]
        
        if pattern == 'solid':
            draw.rectangle([0, 0, 512, 512], fill=color)
        
        elif pattern == 'gradient':
            for y in range(512):
                intensity = int((y / 512) * 255)
                grad_color = tuple(int(c * (intensity / 255)) for c in color)
                draw.line([(0, y), (512, y)], fill=grad_color)
        
        elif pattern == 'circles':
            draw.rectangle([0, 0, 512, 512], fill=(240, 240, 240))
            for r in range(50, 300, 50):
                draw.ellipse([256-r, 256-r, 256+r, 256+r], outline=color, width=5)
        
        elif pattern == 'stripes':
            draw.rectangle([0, 0, 512, 512], fill=(240, 240, 240))
            for x in range(0, 512, 40):
                draw.rectangle([x, 0, x+20, 512], fill=color)
        
        # Add label
        try:
            draw.text((10, 10), f"Image {i+1}", fill='black')
        except:
            pass  # Font might not be available
        
        filename = output_path / f"test_image_{i+1}_{pattern}.png"
        img.save(filename)
        print(f"Created: {filename}")
    
    print(f"\nCreated {num_images} test images in {output_dir}/")
    print(f"You can now run: python immerge.py {output_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create test images for Immerge")
    parser.add_argument("-o", "--output", default="test_images", 
                       help="Output directory (default: test_images)")
    parser.add_argument("-n", "--num", type=int, default=5,
                       help="Number of images to create (default: 5)")
    
    args = parser.parse_args()
    create_test_images(args.output, args.num)
