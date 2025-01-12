import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

def overlay_text_with_background(img, content, coords, font_path, max_width, font_size, text_color, background_color, alpha, padding=10):
    # Convert OpenCV image to PIL image
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), content, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Ensure text fits within max_width
    while text_w > max_width - 2 * padding:
        font_size -= 2
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), content, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Adjust background box to fit text with dynamic padding
    extra_padding = padding + 17  # Increase box height
    box_start_x = coords[0] - padding
    box_start_y = coords[1] - text_h - extra_padding
    box_end_x = coords[0] + text_w + padding
    box_end_y = coords[1] + extra_padding
    
    # Create a semi-transparent overlay for the background
    overlay = Image.new('RGBA', pil_img.size, (0, 0, 0, 0))  # Fully transparent image
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([box_start_x, box_start_y, box_end_x, box_end_y], fill=(*background_color, int(alpha * 255)))
    
    # Blend the overlay with the original image
    pil_img = Image.alpha_composite(pil_img.convert('RGBA'), overlay).convert('RGB')
    
    # Draw the text
    draw = ImageDraw.Draw(pil_img)
    text_x = coords[0]  # Horizontal alignment
    text_y = coords[1] - text_h - 20# Adjust vertical alignment
    draw.text((text_x, text_y), content, font=font, fill=text_color)
    
    # Convert back to OpenCV format
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img

def create_rectangle(img, corner1, corner2, rect_color, line_thickness):
    cv2.rectangle(img, corner1, corner2, rect_color, line_thickness)

# Load image
img = cv2.imread('assignment-001-given.jpg')

# Text details
overlay_text = 'RAH972U'

# Path to the Arial font file
font_path = 'arial.ttf'
font_size = 90
txt_color = (0, 255, 0)
box_color = (18, 17, 17)  # Gray background
transparency = 0.6  # Semi-transparent background
padding_space = 120

# Maximum width for the text box
max_width = 800  # Adjust based on where you want the text to be positioned

# Determine text position
img_h, img_w, _ = img.shape
text_dims, _ = cv2.getTextSize(overlay_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
text_w, text_h = text_dims
text_pos_x = img_w - text_w - padding_space - 180  # Move to the left
text_pos_y = text_h + padding_space + 20  # Move lower for centering

# Add text and rectangle
img = overlay_text_with_background(img, overlay_text, (text_pos_x, text_pos_y), font_path, max_width, font_size, txt_color, box_color, transparency)
create_rectangle(img, (260, 195), (988, 920), (0, 255, 0), 8)

# Display and save image
cv2.imshow('Result Image', img)
cv2.waitKey(0)
cv2.imwrite('assignment-001-result.jpg', img)
cv2.destroyAllWindows()
