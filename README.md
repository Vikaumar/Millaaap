# Milaap - AI-Powered Child Reconnection Platform

Milaap is a secure, state-of-the-art web application designed to reconnect missing individuals and lost children with their families using AI and OpenCV Face Recognition. It includes a secure 2-step permission authentication system via email and real-time GeoIP coordinate tracking.

## Core Features
1. **AI Face Recognition**: Integrates OpenCV's LBPH Face Recognizer to identify registered children.
2. **Dynamic Email Notification**: Alerts the registered parent immediately when their child is identified.
3. **GeoIP Location Tracking**: Captures and embeds the physical coordinates of the scanner location in the parent's email.
4. **Access Protection**: Keeps child details hidden until the parent explicitly approves the request via a secure activation link.
5. **Modern Glassmorphic Dark UI**: Built with a responsive layout, neon glow effects, and modern fonts (Outfit, Plus Jakarta Sans) powered by Bootstrap 5.

## Testability Features
Milaap has been heavily refactored to support testing in environments without access to a physical webcam (e.g., headless testing or VMs):
- **Webcam-Fallback in Registration**: If a physical webcam is not found or fails to read frames during registration training (`/child/congrats/`), the system automatically falls back to extracting the face directly from the child's uploaded profile picture.
- **Webcam-Fallback in Search**: The search scanner (`/child/search/`) features a dual-mode: you can scan via webcam or upload an image file of the child to search and match against the database.

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- A virtual environment is recommended

### Installation Steps
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Vikaumar/Millaaap.git
   cd Milaap
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run Django migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## How to Test

### 1. Account Setup
- Register a new account or log in with the test helper account:
  - **Username**: `head1`
  - **Password**: `pass1234`

### 2. Adding a Child Profile
- From the Dashboard, click **Register Child**.
- Enter the child's details, upload a profile picture, and click **Save and Continue**.
- On the training page, click **Run Training Now**. If you don't have a webcam, the model training will automatically run on the uploaded profile picture using webcam-fallback mode.

### 3. Searching and Face Matching
- From the Dashboard, click **Start Search**.
- Choose your method:
  - **Webcam Scanner**: Click **Open Webcam** to match in real-time.
  - **Image Upload**: Under **Image Upload**, select a photo of the child and click **Upload and Search**.
- Once a match is found:
  - An email containing the matching details and GeoIP location is printed to the console (Django's console email backend).
  - You will see a success message indicating the parent request was initiated.
- Copy the activation URL printed in the console and visit it in the browser to grant access.
- Go back to the dashboard and click **Child Details** (or go to `/child/childdetails/`) to view the fully revealed profile.
