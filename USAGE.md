# Immerge Usage Guide

This guide provides detailed examples and best practices for using Immerge.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Get your OpenAI API key from https://platform.openai.com/api-keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your key
# OPENAI_API_KEY=sk-...your-actual-key-here...
```

### 3. Prepare Your Images

Create a directory with your images:

```bash
mkdir my_images
# Copy your images to my_images/
```

Or use the test image generator:

```bash
python3 setup_example.py -n 10 -o my_images
```

## Usage Examples

### Example 1: Quick Test Run

Run a few iterations to test the setup:

```bash
python3 immerge.py my_images --max-iterations 3 --delay 5
```

This will:
- Run 3 complete iterations
- Wait 5 seconds between iterations
- Save results to the `output` directory
- Generate 9 images total (3 per iteration)

### Example 2: Continuous Generation

Run continuously until you stop it:

```bash
python3 immerge.py my_images
```

Press `Ctrl+C` when you want to stop.

### Example 3: Custom Output Directory

Save generated images to a specific location:

```bash
python3 immerge.py my_images --output ~/Desktop/art_gallery
```

### Example 4: Longer Delays

Give yourself time to review each iteration:

```bash
python3 immerge.py my_images --max-iterations 10 --delay 30
```

This waits 30 seconds between iterations.

### Example 5: Overnight Generation

Run many iterations with longer delays for cost control:

```bash
python3 immerge.py my_images --max-iterations 50 --delay 60
```

This will:
- Run 50 iterations
- Generate 150 images total
- Take about 50+ minutes (excluding API time)
- Cost approximately $6 in API fees

## Understanding the Process

### What Happens in Each Iteration

1. **Random Selection #1**: 2-10 images randomly selected
2. **Grid Creation #1**: Images arranged in a grid
3. **AI Generation #1**: DALL-E 3 creates "new image #1" inspired by the grid
4. **Random Selection #2**: 1-7 images randomly selected
5. **Grid Creation #2**: Images arranged in a grid
6. **AI Generation #2**: DALL-E 3 creates "new image #2" inspired by the grid
7. **Style Transfer**: DALL-E 3 creates final image combining content from #1 with style from #2

### Output Files

Each iteration creates multiple files:

```
output/
├── combined_iter1_1234567890.png  # Grid of source images for new image #1
├── new_image_1_iter1.png          # AI-generated composition #1
├── combined_iter1_1234567891.png  # Grid of source images for new image #2
├── new_image_2_iter1.png          # AI-generated composition #2
└── styled_iter1.png               # Final result with style transfer
```

## Cost Management

### Understanding API Costs

- **DALL-E 3 Standard Quality (1024x1024)**: $0.040 per image
- **Images per iteration**: 3 (new image #1, new image #2, styled result)
- **Cost per iteration**: ~$0.12
- **Cost for 10 iterations**: ~$1.20
- **Cost for 100 iterations**: ~$12.00

### Tips to Control Costs

1. **Set Max Iterations**
   ```bash
   python3 immerge.py my_images --max-iterations 10
   ```

2. **Start Small**
   - Test with 2-3 iterations first
   - Review the results before running longer sessions

3. **Monitor Your Usage**
   - Check OpenAI usage dashboard: https://platform.openai.com/usage
   - Set billing limits in your OpenAI account

4. **Use Delays Wisely**
   - Longer delays don't reduce costs but give you time to stop if needed
   - Shorter delays generate more images faster (and incur costs faster)

## Best Practices

### Choosing Source Images

1. **Variety is Key**
   - Use images with different colors, styles, and subjects
   - Mix photos, illustrations, abstract art, patterns

2. **Minimum Count**
   - Need at least 2 images
   - Recommend 8+ for better variety
   - Sweet spot: 10-20 images

3. **Image Quality**
   - Use high-quality source images
   - Images are resized to 1024x1024 maximum
   - Supported formats: JPG, PNG, WebP, GIF

### Organizing Results

The output directory can get large quickly. Consider:

```bash
# Create dated output directories
python3 immerge.py my_images --output output_$(date +%Y%m%d)

# Or by session
python3 immerge.py my_images --output session_1
```

### Stopping the Application

Always stop with `Ctrl+C` rather than force-killing:
- Allows current API call to complete
- Prevents partial/corrupt files
- Displays summary statistics

## Advanced Usage

### Using with Different Image Sets

Run multiple sessions with different image collections:

```bash
# Nature theme
python3 immerge.py ~/images/nature --output output_nature --max-iterations 5

# Abstract art theme
python3 immerge.py ~/images/abstract --output output_abstract --max-iterations 5

# Mixed theme
python3 immerge.py ~/images/mixed --output output_mixed --max-iterations 5
```

### Batch Processing

Create a script for multiple runs:

```bash
#!/bin/bash
for i in {1..5}; do
  echo "Session $i"
  python3 immerge.py my_images --max-iterations 10 --output "session_$i"
  echo "Session $i complete. Waiting 5 minutes..."
  sleep 300
done
```

### Quick Start Script

Use the included quick start script:

```bash
# Setup with test images
./quickstart.sh

# Then run
python3 immerge.py test_images --max-iterations 3
```

## Troubleshooting

### "No module named 'dotenv'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"

Check your .env file:
```bash
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### "Need at least 2 images"

Add more images to your input directory:
```bash
python3 setup_example.py -n 10 -o my_images
```

### API Rate Limits

If you hit rate limits, increase the delay:
```bash
python3 immerge.py my_images --delay 10
```

### Out of Memory

If processing very large images, they're automatically resized to 1024x1024 maximum.

## FAQ

**Q: Can I use my own images?**
A: Yes! Any JPG, PNG, WebP, or GIF images work.

**Q: How long does each iteration take?**
A: Typically 30-60 seconds per iteration, depending on API response times.

**Q: Can I pause and resume?**
A: No, but you can stop with Ctrl+C and start a new session anytime.

**Q: Where do the generated images go?**
A: By default to the `output/` directory, or specify with `--output`.

**Q: Can I use a different AI model?**
A: The code currently uses DALL-E 3. You can modify the code to use other APIs.

**Q: Does it need internet?**
A: Yes, it requires internet to access the OpenAI API.

**Q: What if I run out of API credits?**
A: The app will show an error. Add credits to your OpenAI account and restart.

## Support

For issues, questions, or contributions, please visit:
https://github.com/flypaper-creative/Immerge
