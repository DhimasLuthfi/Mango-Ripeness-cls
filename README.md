# 🥭 Mango Ripeness Classifier (YOLOv8)

## Project Description
This project is an intelligent Computer Vision web application designed to automate the identification of mango ripeness levels. Powered by a highly optimized **YOLOv8-cls** deep learning model with custom visual augmentations, the app can classify 4 distinct stages of mango ripeness in real-time using uploaded photos or a live webcam feed.

## Key Features
* **Real-Time Classification**: Delivers accurate predictions in milliseconds.
* **Multi-Input Support**: Users can upload local images (JPG/PNG) or capture photos directly via the Streamlit webcam interface.
* **Probability Visualization**: Displays the AI's confidence scores for all four ripeness stages using interactive progress bars.
* **Memory-Efficient**: Ensures data privacy and resource efficiency by processing all images in-memory without saving them to the server.

## Ripeness Classes
1. **Unripe**: Hard green mangoes.
2. **Early Ripe**: Green mangoes with slight yellowish tints.
3. **Partially Ripe**: Evenly mixed green and yellow colors.
4. **Ripe**: Pale reddish-orange or fully yellow mangoes.

## Tech Stack
* **Machine Learning**: Ultralytics YOLOv8 (Image Classification)
* **Frontend UI**: Streamlit Community Cloud
* **Image Processing**: OpenCV & Pillow
* **Data Manipulation**: NumPy

## Local Setup Instructions
1. Clone this repository.
2. Create a virtual environment: `python -m venv env`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Place your trained model weights (`best.pt`) in the root directory.
5. Run the application: `streamlit run app.py`