from flask import Flask, request, render_template , jsonify
import firebase_admin
from firebase_admin import credentials, firestore, storage
import cv2
import uuid
from PIL import Image
import img2pdf
import os

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("keys/serviceAccountKey.json")  # Use forward slashes for paths on all platforms
firebase_admin.initialize_app(cred, {
    'storageBucket': 'certificate-generator-2c25e.appspot.com'  # Replace with your actual bucket name
})

db = firestore.client()
bucket = storage.bucket()

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

        return pdf_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    name = request.form.get('NAME')
    email = request.form.get('EMAIL')

    if len(name) > 20:
        return jsonify({"error": "Name must be less than 20 characters"}), 400

    # Create the certificate
    candidate_id = str(uuid.uuid4())

    # Add candidate name to the certificate
    pdf_path = add_text_to_certificate(name, candidate_id)

    if pdf_path is None:
        return jsonify({"error": "Failed to create certificate"}), 500

    # Upload to Firebase Storage
    blob = bucket.blob(f"certificates/{candidate_id}.pdf")
    blob.upload_from_filename(pdf_path, content_type='application/pdf')

    # Get the public URL
    blob.make_public()
    certificate_url = blob.public_url

    # Store metadata in Firestore
    doc_ref = db.collection('certificates').document(candidate_id)
    doc_ref.set({
        'name': name,
        'certificate_url': certificate_url,
        'email': email
    })

    html_content = f'''
    <html>
        <body style="text-align: center;">
            <br><BR>
            <h1 > Congratulation </h1>
            <br>
            <p style="font-size: 20px;">Here is your <a href={certificate_url}>certificate </a> </p>
            <P> click to download it </P>
            
        </body>
    </html>
    '''

    return html_content

    #return jsonify({"certificate_url": certificate_url}), 200

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/search_certificate', methods=['GET'])
def view_certificate():
    name1 = request.args.get('NAME')
    certificate_id = request.args.get('ID')
    print(certificate_id)
    doc_ref = db.collection('certificates').document(certificate_id)
    
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"error": "Certificate not found"}), 404

    certificate_url = doc.to_dict().get('certificate_url')
    certificate_name = doc.to_dict().get('name')
    print(certificate_name)

    html_content = f'''
    <html>
        <body>
            <iframe src="{certificate_url}" width="100%" height="100%" frameborder="0">
                This browser does not support PDFs. Please download the PDF to view it: <a href="{certificate_url}">Download PDF</a>
            </iframe>
        </body>
    </html>
    '''

    return html_content

if __name__ == '__main__':
    app.run(debug=True)
