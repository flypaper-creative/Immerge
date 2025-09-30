# Immerge

AI-powered image generation and merging application that continuously creates unique artworks by combining and stylizing images using OpenAI's DALL-E API.

## Overview

Immerge is an automated image generation tool that:
1. Randomly selects 2-10 images from your collection and merges them into a new composition (new image #1)
2. Randomly selects 1-7 images and merges them into another composition (new image #2)
3. Applies the visual style of new image #2 to new image #1
4. Repeats this process continuously until stopped

## Features

- 🎨 AI-powered image generation using OpenAI's DALL-E 3
- 🔀 Random selection of source images for endless variety
- 🖼️ Automatic image combination and grid layout generation
- 🎭 Style transfer between generated images
- ⚡ Continuous generation loop with configurable delays
- 📁 Organized output directory structure
- 🛑 Graceful stop with Ctrl+C

## Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to DALL-E 3
- Input images in supported formats (JPG, PNG, WebP, GIF)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/flypaper-creative/Immerge.git
cd Immerge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

```bash
python immerge.py /path/to/your/images
```

This will:
- Load all images from the specified directory
- Start generating images continuously
- Save output to the `output` directory
- Run until you press Ctrl+C

### Advanced Options

```bash
python immerge.py /path/to/your/images \
  --output custom_output_dir \
  --max-iterations 10 \
  --delay 10
```

**Arguments:**
- `image_dir` (required): Directory containing input images
- `-o, --output`: Output directory for generated images (default: `output`)
- `-n, --max-iterations`: Maximum number of iterations (default: infinite)
- `-d, --delay`: Delay in seconds between iterations (default: 5.0)

### Example

```bash
# Run 5 iterations with 30-second delays
python immerge.py ./my_images --max-iterations 5 --delay 30

# Run continuously with output to custom directory
python immerge.py ./my_images --output ./generated_art
```

## How It Works

### Iteration Process

Each iteration follows these steps:

1. **Image Selection #1**: Randomly select 2-10 images from your collection
2. **Combination #1**: Combine selected images into a grid layout
3. **Generation #1**: Use DALL-E 3 to generate "new image #1" inspired by the combination
4. **Image Selection #2**: Randomly select 1-7 images from your collection
5. **Combination #2**: Combine selected images into a grid layout
6. **Generation #2**: Use DALL-E 3 to generate "new image #2" inspired by the combination
7. **Style Transfer**: Generate a final image that applies the style of new image #2 to the content of new image #1

### Output Structure

Generated images are saved in the output directory with descriptive names:
```
output/
├── combined_iter1_1234567890.png      # Combined grid of source images
├── new_image_1_iter1.png              # First generated composition
├── new_image_2_iter1.png              # Second generated composition
├── styled_iter1.png                   # Final styled result
├── combined_iter2_1234567891.png      # Next iteration...
└── ...
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Image Requirements

- Minimum 2 images required in the input directory
- Supported formats: JPG, JPEG, PNG, WebP, GIF
- Images are automatically resized and formatted for the API
- RGBA images are converted to RGB with white background

## API Costs

**Important:** This application uses OpenAI's DALL-E 3 API, which has associated costs:
- DALL-E 3 (1024x1024): $0.040 per image
- Each iteration generates 3 images (new image #1, new image #2, and styled result)
- Cost per iteration: ~$0.12

Monitor your usage and set appropriate `--max-iterations` limits to control costs.

## Stopping the Application

Press `Ctrl+C` at any time to gracefully stop the generation loop. The application will:
- Complete the current API call
- Display statistics about completed iterations
- Exit cleanly

## Troubleshooting

### "OPENAI_API_KEY not found"
Make sure you've created a `.env` file with your API key.

### "Need at least 2 images"
Ensure your input directory contains at least 2 valid image files.

### API Errors
- Check your OpenAI API key is valid and has credits
- Verify you have access to DALL-E 3
- Check your internet connection

### Rate Limiting
If you encounter rate limits, increase the `--delay` parameter to add more time between iterations.

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with OpenAI's DALL-E 3 API
- Uses Pillow for image processing