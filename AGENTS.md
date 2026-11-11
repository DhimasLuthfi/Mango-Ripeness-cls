# Antigravity Agent Guidelines: Mango Ripeness Classifier

## 1. Agent Role
You are acting as a **Senior Computer Vision & Python Developer**. Your task is to integrate a YOLOv8-cls (image classification) model into a Streamlit web interface. You must write clean (PEP 8 compliant), modular, and efficient code with proper `try-except` error handling.

## 2. Technology Stack
* **Frontend & Framework**: Streamlit (`streamlit`)
* **Machine Learning Engine**: Ultralytics YOLOv8 (`ultralytics`)
* **Image Processing**: Pillow (`PIL`), OpenCV (`opencv-python-headless`)
* **Data Manipulation**: NumPy (`numpy`)
* **Language**: Python 3.9+

## 3. Environment & Project Structure
The project MUST follow this exact directory structure to ensure clean deployment to Streamlit Community Cloud. Do not create unnecessary boilerplate folders.

```text
mango-ripeness-app/
├── app.py                 # (Required) Main Streamlit entry point.
├── best.pt                # (Provided by User) YOLOv8-cls model weights.
├── requirements.txt       # (Required) Python dependencies.
├── .gitignore             # (Required) Excludes cache and environment files.
├── README.md              # (Provided) Project documentation.
├── design.md              # (Provided) UI/UX styling guidelines.
└── assets/                # (Optional) For storing logos or sample images.
```

## 4. Deep Learning Specifications
* **Model Engine**: Ultralytics YOLOv8 (Image Classification mode).
* **Weights File**: `best.pt` (MUST be loaded using Streamlit's `@st.cache_resource` decorator to prevent memory leaks).
* **Target Classes (4 Stages)**:
  0. `Stage_0 (Unripe)`
  1. `Stage_1 (Early Ripe)`
  2. `Stage_2 (Partially Ripe)`
  3. `Stage_3 (Ripe)`
* **Inference Behavior**: The model receives an RGB image matrix (NumPy array) and returns the predicted class with the highest probability (Top-1) along with its Confidence Score.

## 5. System Constraints
* **No File Saving**: The application MUST NOT save any user-uploaded images to local storage. All image processing must occur entirely in memory (RAM) using `PIL.Image`.
* **Lightweight Dependencies**: Do not use heavy libraries like `tensorflow` or `keras`. Stick strictly to the defined tech stack.
* **Error Handling**: If a user uploads an invalid file format or if the webcam is unavailable, handle it gracefully using `st.warning` or `st.error`. The application must never crash.

## 6. Git Commit Message Conventions
All agents **MUST** follow a strict conventional commit format **without scopes**. Consistency is essential for clean collaboration and history readability.

### Format
<type>: <short imperative description>

[optional longer description / body explaining why and what changed]

### Strict Rules
1. **NEVER use scopes in parentheses (`(scope)`):**
   - ✅ **CORRECT:** `feat: add result.html prototype with interactive red flag bounding boxes`
   - ❌ **INCORRECT:** `feat(proto): add result.html prototype with interactive red flag bounding boxes`
2. **Use imperative mood in lowercase** for the commit subject (`add`, `fix`, `update`, `remove`, `refactor`).
3. **No trailing punctuation:** Do not end the commit subject with a period (`.`).
4. **Subject line length:** Keep the first line under 72 characters when possible.
5. **Body (optional):** Separate the subject from the body with a blank line.

### Allowed Types
* `feat`: New feature or user-facing addition
* `fix`: Bug fix or visual correction
* `docs`: Documentation changes only
* `style`: Formatting or styling without logic changes
* `refactor`: Code restructuring without adding features or fixing bugs
* `perf`: Performance improvements
* `test`: Adding or modifying tests
* `chore`: Maintenance, configuration, dependencies, or tooling