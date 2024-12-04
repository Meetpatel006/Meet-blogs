import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\hites\Documents\Meet Blog\content\posts"
attachments_dir = r"C:\Users\hites\Documents\Project Ideas"
static_images_dir = r"C:\Users\hites\Documents\Meet Blog\static\images"

# Supported image extensions
valid_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format [[filename.ext]]
        images = re.findall(r'\[\[([^]]+\.(?:png|jpg|jpeg|gif|bmp|webp))\]\]', content, re.IGNORECASE)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory
            image_source = os.path.join(attachments_dir, image)
            image_dest = os.path.join(static_images_dir, os.path.basename(image))
            
            # Ensure the source exists and copy
            if os.path.exists(image_source):
                try:
                    shutil.copy(image_source, image_dest)
                except Exception as e:
                    print(f"Error copying {image_source} to {image_dest}: {e}")
            else:
                print(f"Source file does not exist: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
