# UI/UX & Visualization Guidelines: Mango Ripeness Classifier

## 1. Overall Theme & Layout
* **Framework**: Streamlit native components.
* **Layout Structure**: Use a multi-column approach (`st.columns`) for the main results page. Place the original input image on the left column and the classification results/metrics on the right column.
* **Tone**: Professional, clean, and user-friendly. Use relevant emojis (like 🥭) sparingly in headers to make the UI engaging but not cluttered.

## 2. Interactive Components
* **Input Methods**: Provide clear options for users using `st.radio` or `st.tabs` to switch between "Upload Image" and "Camera Input".
* **Loaders**: Use `st.spinner` with a descriptive message (e.g., "Analyzing ripeness...") during model inference to provide visual feedback to the user.

## 3. Data Visualization & Metrics
* **Primary Result**: Highlight the Top-1 predicted class using `st.success` (for valid predictions) and a prominent `st.metric` component to display the exact Confidence Score percentage.
* **Probability Distribution**: Render the probabilities of all 4 classes using `st.progress` bars or `st.bar_chart`. This helps the user understand the model's decision-making process (e.g., showing a 60% chance of Partially Ripe and a 40% chance of Ripe).

## 4. UX Safeguards & Warnings
* **Low Confidence Threshold**: If the Top-1 Confidence Score falls below 50%, trigger an `st.info` or `st.warning` message alerting the user that the image might not be a mango, might be too blurry, or suffers from poor lighting conditions.
* **Empty States**: Do not show the results container or error messages before the user has submitted an image.