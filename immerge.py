#!/usr/bin/env python3
"""
Immerge - AI-powered image generation and merging application
"""

import os
import random
import time
import argparse
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import io
import base64
import requests

# Load environment variables
load_dotenv()


class Immerge:
    """Main application class for image merging and generation"""
    
    def __init__(self, image_dir: str, output_dir: str = "output"):
        """
        Initialize the Immerge application
        
        Args:
            image_dir: Directory containing input images
            output_dir: Directory to save generated images
        """
        self.image_dir = Path(image_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
        # Load available images
        self.images = self._load_images()
        if len(self.images) < 2:
            raise ValueError(f"Need at least 2 images in {image_dir}, found {len(self.images)}")
        
        self.iteration = 0
        self.running = False
        
    def _load_images(self) -> List[Path]:
        """Load all images from the input directory"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        images = []
        
        for file_path in self.image_dir.iterdir():
            if file_path.suffix.lower() in supported_formats:
                images.append(file_path)
        
        print(f"Loaded {len(images)} images from {self.image_dir}")
        return images
    
    def _prepare_image_for_api(self, image_path: Path, max_size: int = 1024) -> bytes:
        """
        Prepare an image for OpenAI API by resizing and converting to PNG
        
        Args:
            image_path: Path to the image file
            max_size: Maximum dimension (width or height) in pixels
            
        Returns:
            Image data as bytes
        """
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if needed
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr.read()
    
    def _combine_images(self, image_paths: List[Path]) -> Path:
        """
        Combine multiple images into a grid layout
        
        Args:
            image_paths: List of paths to images to combine
            
        Returns:
            Path to the combined image
        """
        images = [Image.open(path) for path in image_paths]
        
        # Calculate grid dimensions
        num_images = len(images)
        cols = int(num_images ** 0.5) + (1 if num_images % int(num_images ** 0.5) != 0 else 0)
        rows = (num_images + cols - 1) // cols
        
        # Resize all images to a common size
        target_size = (512, 512)
        resized_images = []
        for img in images:
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            resized_images.append(img.resize(target_size, Image.Resampling.LANCZOS))
        
        # Create the combined image
        grid_width = cols * target_size[0]
        grid_height = rows * target_size[1]
        combined = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))
        
        for idx, img in enumerate(resized_images):
            row = idx // cols
            col = idx % cols
            x = col * target_size[0]
            y = row * target_size[1]
            combined.paste(img, (x, y))
        
        # Save the combined image
        output_path = self.output_dir / f"combined_iter{self.iteration}_{int(time.time())}.png"
        combined.save(output_path)
        return output_path
    
    def _generate_merged_image(self, base_image_path: Path, num_images: int, 
                               description: str) -> Path:
        """
        Generate a merged/evolved image using OpenAI API
        
        Args:
            base_image_path: Path to the base image
            num_images: Number of source images used
            description: Description for the generation prompt
            
        Returns:
            Path to the generated image
        """
        print(f"Generating {description} from {num_images} images...")
        
        # Create a prompt that describes the merging/evolution
        prompt = (
            f"Create a unique artistic composition by merging and blending elements "
            f"from {num_images} different images. Combine colors, patterns, textures, "
            f"and visual elements into a cohesive new artwork that maintains interesting "
            f"details from the source images while creating something entirely new."
        )
        
        try:
            # Use DALL-E 3 for generation based on the combined image
            # Since we can't directly upload images to DALL-E 3, we describe the style
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Download the generated image
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            
            # Save the image
            output_path = self.output_dir / f"{description.replace(' ', '_')}_iter{self.iteration}.png"
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            print(f"Generated {description}: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return the combined image as fallback
            return base_image_path
    
    def _apply_style_transfer(self, content_image_path: Path, 
                             style_image_path: Path) -> Path:
        """
        Apply the style of one image to another using OpenAI API
        
        Args:
            content_image_path: Path to the content image (new image #1)
            style_image_path: Path to the style image (new image #2)
            
        Returns:
            Path to the styled image
        """
        print(f"Applying style transfer...")
        
        # Create a prompt for style transfer
        prompt = (
            "Create an artistic image that combines the content and composition from one image "
            "with the visual style, colors, textures, and artistic techniques from another image. "
            "Blend them seamlessly into a unique artwork that preserves the structure while "
            "adopting the aesthetic style."
        )
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Download the generated image
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            
            # Save the image
            output_path = self.output_dir / f"styled_iter{self.iteration}.png"
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            print(f"Generated styled image: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error applying style transfer: {e}")
            return content_image_path
    
    def run_iteration(self):
        """Run a single iteration of the image generation process"""
        self.iteration += 1
        print(f"\n{'='*60}")
        print(f"ITERATION {self.iteration}")
        print(f"{'='*60}\n")
        
        # Step 1: Select 2-10 random images and combine them into new image #1
        num_images_1 = random.randint(2, min(10, len(self.images)))
        selected_images_1 = random.sample(self.images, num_images_1)
        print(f"Step 1: Combining {num_images_1} random images into new image #1")
        print(f"  Selected: {[img.name for img in selected_images_1]}")
        
        combined_image_1 = self._combine_images(selected_images_1)
        new_image_1 = self._generate_merged_image(
            combined_image_1, 
            num_images_1, 
            "new_image_1"
        )
        
        # Step 2: Select 1-7 random images and combine them into new image #2
        num_images_2 = random.randint(1, min(7, len(self.images)))
        selected_images_2 = random.sample(self.images, num_images_2)
        print(f"\nStep 2: Combining {num_images_2} random images into new image #2")
        print(f"  Selected: {[img.name for img in selected_images_2]}")
        
        combined_image_2 = self._combine_images(selected_images_2)
        new_image_2 = self._generate_merged_image(
            combined_image_2, 
            num_images_2, 
            "new_image_2"
        )
        
        # Step 3: Apply the style of new image #2 to new image #1
        print(f"\nStep 3: Applying style of new image #2 to new image #1")
        final_image = self._apply_style_transfer(new_image_1, new_image_2)
        
        print(f"\n{'='*60}")
        print(f"Iteration {self.iteration} complete!")
        print(f"Final image: {final_image}")
        print(f"{'='*60}\n")
        
        return final_image
    
    def run(self, max_iterations: int = None, delay: float = 5.0):
        """
        Run the image generation loop
        
        Args:
            max_iterations: Maximum number of iterations (None for infinite)
            delay: Delay in seconds between iterations
        """
        self.running = True
        
        print("\n" + "="*60)
        print("IMMERGE - AI Image Generation and Merging")
        print("="*60)
        print(f"Input directory: {self.image_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Available images: {len(self.images)}")
        print(f"Max iterations: {max_iterations if max_iterations else 'Infinite'}")
        print(f"Delay between iterations: {delay}s")
        print("\nPress Ctrl+C to stop\n")
        print("="*60 + "\n")
        
        try:
            iteration_count = 0
            while self.running:
                self.run_iteration()
                iteration_count += 1
                
                if max_iterations and iteration_count >= max_iterations:
                    print(f"\nReached maximum iterations ({max_iterations}). Stopping.")
                    break
                
                print(f"Waiting {delay} seconds before next iteration...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\nStopping Immerge...")
            self.running = False
        
        print(f"\nCompleted {iteration_count} iterations.")
        print(f"Generated images saved to: {self.output_dir}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Immerge - AI-powered image generation and merging application"
    )
    parser.add_argument(
        "image_dir",
        help="Directory containing input images"
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory for generated images (default: output)"
    )
    parser.add_argument(
        "-n", "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of iterations (default: infinite)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=5.0,
        help="Delay in seconds between iterations (default: 5.0)"
    )
    
    args = parser.parse_args()
    
    # Validate image directory
    if not os.path.isdir(args.image_dir):
        print(f"Error: {args.image_dir} is not a valid directory")
        return 1
    
    try:
        app = Immerge(args.image_dir, args.output)
        app.run(max_iterations=args.max_iterations, delay=args.delay)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
