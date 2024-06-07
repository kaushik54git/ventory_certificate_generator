import cv2
import uuid
from PIL import Image
import img2pdf
import os

def add_text_to_certificate(candidate_name, candidate_id):
    # Define certificate image path
    certificate_image_path = 'Python Team/Code Snippets/blank_certificate.png'

    # Define y axis for text placement
    y = 725

    # Define font-related parameters
    font_scale = 4  # Font size
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX  # Font style
    thickness = 4  # Font weight
    color = (0, 0, 0)  # Font color

    # Load the image
    image = cv2.imread(certificate_image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Could not open or find the image at path: {certificate_image_path}")
        return

    # Get the width and height of the image
    (image_height, image_width) = image.shape[:2]

    # Get the text size
    text_size = cv2.getTextSize(candidate_name, font, font_scale, thickness)[0]

    # Calculate the x coordinate to center the text
    text_x = (image_width - text_size[0]) // 2

    # Put the text on the image
    cv2.putText(image, candidate_name, (text_x, y), font, font_scale, color, thickness)

    # Ensure the temporary directory exists
    os.makedirs('temporary', exist_ok=True)
    # Store the image in the temporary directory
    png_output_path = f"temporary/{candidate_id}.png"
    cv2.imwrite(png_output_path, image)

    # Ensure the output_pdfs directory exists
    os.makedirs('output_pdfs', exist_ok=True)
    # Convert the cv2 image to PDF and save it in the output_pdfs directory
    pdf_path = f"output_pdfs/{candidate_id}.pdf"

    try:
        # Open the image
        with Image.open(png_output_path) as img:
            # Convert the image to PDF bytes
            pdf_bytes = img2pdf.convert(img.filename)

            # Write the PDF bytes to a file
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_bytes)

        print(f"Certificate saved at: {pdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Usage example
    candidate_name = "Kaushik Kumbhat"
    candidate_id = str(uuid.uuid4())

    # Add candidate name to the certificate
    add_text_to_certificate(candidate_name, candidate_id)
