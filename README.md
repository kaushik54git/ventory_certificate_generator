# Certificate Generator

## Overview

The Certificate Generator is a web-based application built with Python Flask that allows users to generate personalized certificates. Users can input their name and email, and the application will create a customized certificate, store it in Google Firebase Storage, and keep the metadata in Firestore. The generated certificate can be accessed and viewed through a unique URL.

## Features

- **Personalized Certificate Generation**: Users can input their name and email to generate a custom certificate.
- **Certificate Search**: Users can input their name or certificate ID to retrive their certificate.
- **Firebase Integration**: The application uses Firebase Cloud Storage for storing certificate images and Firestore for storing metadata.
- **Web Interface**: A simple and intuitive web interface for users to generate and view their certificates.
- **Secure Storage**: All certificates are securely stored in Firebase's Cloud Storage with public URLs for easy access.

## Technologies Used

- **Flask**: Python-based micro web framework for handling the backend.
- **OpenCV**: Library for adding text to the certificate image.
- **Pillow**: Python Imaging Library (PIL) for image processing.
- **img2pdf**: Tool for converting images to PDF format.
- **Firebase**: Google Firebase for backend as a service, including Firestore and Cloud Storage.

## Prerequisites

- Python 3.6 or above
- Firebase Account with Firestore and Cloud Storage setup
- Firebase Admin SDK Service Account Key

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaushik54git/ventory_certificate_generator.git
   cd ventory_certificate_generator
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Firebase Setup**:
   - Obtain your Firebase Admin SDK Service Account Key and save it as `serviceAccountKey.json` in the `keys` directory.
   - Update the Firebase project ID and storage bucket in `main.py`.

5. **Run the Application**:
   ```bash
   flask run
   ```

6. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Generate Certificate**:
   - Open the application in your browser.
   - Enter your name and email in the form.
   - Click "Generate Certificate".
   - The application will create a personalized certificate and display a link to view it.

2. **View Certificate**:
   - After generating the certificate, a unique URL will be provided.
   - Click the link to view your certificate.
  
3. **Certificate Search**:
   - Go to `http://127.0.0.1:5000/search`.
   - Enter your name or Certificate ID in the form.
   - Click "Search".
   - The application will retrieve your certificate and display to view it.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or feedback, please contact:

Kaushik Kumbhat  
[GitHub](https://github.com/kaushik54git)  
