from pathlib import Path
import re
from PIL import Image

def process_markdown(input_file, target_width):
    # Read the markdown file
    content = Path(input_file).read_text()
    
    # Regular expression to find markdown images
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        try:
            # Open the image and get its width
            with Image.open(img_path) as img:
                original_width = img.size[0]
            
            # Calculate scale factor as percentage
            scale_factor = (target_width / original_width) * 100
            
            # Create new HTML img tag with zoom
            return f'<img src="{img_path}" alt="{alt_text}" style="zoom:{scale_factor:.2f}%;" />'
            
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
            return match.group(0)  # Return original if there's an error
    
    # Replace all images in the content
    new_content = re.sub(img_pattern, replace_image, content)
    
    # Write back to file (you might want to create a new file instead)
    output_file = input_file.replace('.md', '_processed.md')
    Path(output_file).write_text(new_content)
    
    return output_file

# Example usage
if __name__ == "__main__":
    input_file = "Guide to Typebot.md"
    target_width = 450  # desired width in pixels
    
    output_file = process_markdown(input_file, target_width)
    print(f"Processed file saved as: {output_file}")