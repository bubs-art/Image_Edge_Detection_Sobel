# Image Edge Detection using Sobel Filter and PyTorch

A simple image-processing web application that detects edges in uploaded images using the **Sobel edge detection operator** and **PyTorch**. The interface is built with Streamlit and features a dark purple/magenta GPU-themed design.

## Features

- Upload images in PNG, JPG, JPEG, BMP, or WEBP format.
- Convert the uploaded image to grayscale.
- Apply Sobel X and Sobel Y convolution filters.
- Combine the horizontal and vertical gradients to produce an edge map.
- View the grayscale original and detected edges side by side.
- View image dimensions, processing time, and the compute device used.
- Download the edge-detected image as a PNG file.
- Automatically use CUDA when a CUDA-capable PyTorch environment is available; otherwise, use the CPU.
- Full-page GPU background artwork with a scroll-linked clockwise rotation effect in supported browsers.

## Technology Stack

- **Python** – application and image-processing logic
- **Streamlit** – web interface
- **PyTorch** – convolution operations and device handling
- **NumPy** – image-array processing
- **Pillow (PIL)** – image loading, conversion, and saving
- **HTML/CSS** – visual styling and scroll-linked background animation

## Project Structure

```text
Image_Edge_Detection_Streamlit_App/
├── app.py              # Streamlit frontend and application flow
├── backend.py          # Sobel edge-detection implementation
├── gpu_card.png        # GPU background artwork
└── requirements.txt    # Python dependencies
```

## How It Works

The application uses the Sobel operator to estimate image intensity changes in the horizontal and vertical directions.

1. **Upload:** The user selects an image through the Streamlit file uploader.
2. **Grayscale conversion:** The image is converted to a single-channel grayscale image.
3. **Tensor conversion:** Pixel values are converted into a PyTorch tensor and normalized to the range 0–1.
4. **Sobel X:** A horizontal Sobel kernel is applied using a 2D convolution.
5. **Sobel Y:** A vertical Sobel kernel is applied using a 2D convolution.
6. **Gradient magnitude:** The two responses are combined using:

   \[
   G = \sqrt{G_x^2 + G_y^2}
   \]

7. **Normalization:** The gradient magnitude is normalized to create an 8-bit grayscale edge image.
8. **Display and download:** The app displays the original grayscale image and edge map, then lets the user download the result.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the repository URL and folder name with your own GitHub details.

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
streamlit
torch
numpy
Pillow
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## CPU and GPU Support

The application checks whether CUDA is available through PyTorch:

- If CUDA is available, the backend uses the CUDA device.
- If CUDA is unavailable, the backend automatically uses the CPU.

**Note:** CUDA requires a compatible NVIDIA GPU, driver, and CUDA-enabled PyTorch installation. Standard macOS systems generally run this project on the CPU; Apple Silicon users may need a separately configured PyTorch MPS implementation to use the Apple GPU. The current code checks CUDA only and does not select MPS.

## GPU Background Animation

The frontend includes a full-page GPU background image with its opacity set to 50%. Its clockwise rotation is linked to the scroll progress of Streamlit's main content area.

The scroll-driven animation requires a recent Chromium-based browser, such as Google Chrome or Microsoft Edge, with CSS scroll-driven animation support. Browser accessibility settings that request reduced motion may disable the animation.

## Output

After uploading an image, the application displays:

- The grayscale original image
- The Sobel edge-detected image
- Image width and height
- Processing time
- The compute device used

The edge map can be downloaded as `edge_detected_output.png`.

## Troubleshooting

### `ModuleNotFoundError: No module named 'torch'`

Activate the project's virtual environment and install the requirements:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment using:

```powershell
venv\Scripts\Activate.ps1
```

### Streamlit command not found

Run Streamlit through the active Python environment:

```bash
python -m streamlit run app.py
```

### GPU processing is not selected

Check CUDA availability:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If the result is `False`, the application uses the CPU.

## Future Improvements

- Add adjustable edge-detection thresholds.
- Support additional edge-detection algorithms such as Canny and Prewitt.
- Add image resizing and batch processing.
- Add Apple Silicon MPS device support.
- Compare CPU and GPU processing times on compatible hardware.

## Project Information

**Project:** Image Edge Detection using Sobel Filter and PyTorch  
**Frontend:** Streamlit  
**Backend:** Python and PyTorch  
**Algorithm:** Sobel Edge Detection

---

*Created as a mini project to demonstrate image processing, convolution filters, and CPU/GPU computing concepts.*
