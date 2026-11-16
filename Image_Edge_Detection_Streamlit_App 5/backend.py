"""
Backend for Image Edge Detection using the Sobel filter and PyTorch.
This file contains the image-processing logic only; the Streamlit UI is in app.py.
"""

import time
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

SOBEL_X = torch.tensor(
    [[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]],
    dtype=torch.float32
).unsqueeze(0)

SOBEL_Y = torch.tensor(
    [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]]],
    dtype=torch.float32
).unsqueeze(0)


def detect_edges(image: Image.Image, device: str = "cpu"):
    """
    Convert an image to grayscale and detect edges using Sobel X and Y filters.

    Returns:
        original_gray: grayscale PIL image
        edge_image: edge result as an 8-bit grayscale PIL image
        details: dictionary containing device, image size, and processing time
    """
    if image is None:
        raise ValueError("Please provide an image.")

    original_gray = image.convert("L")
    image_array = np.asarray(original_gray, dtype=np.float32) / 255.0
    image_tensor = torch.from_numpy(image_array).unsqueeze(0).unsqueeze(0)

    selected_device = torch.device(device)
    image_tensor = image_tensor.to(selected_device)
    filter_x = SOBEL_X.to(selected_device)
    filter_y = SOBEL_Y.to(selected_device)

    if selected_device.type == "cuda":
        torch.cuda.synchronize()

    start_time = time.perf_counter()

    edges_x = F.conv2d(image_tensor, filter_x, padding=1)
    edges_y = F.conv2d(image_tensor, filter_y, padding=1)
    edge_strength = torch.sqrt(edges_x ** 2 + edges_y ** 2)
    edge_strength = edge_strength / (edge_strength.max() + 1e-8)

    if selected_device.type == "cuda":
        torch.cuda.synchronize()

    processing_time = time.perf_counter() - start_time

    edge_array = (
        edge_strength.squeeze().detach().cpu().numpy() * 255
    ).clip(0, 255).astype(np.uint8)

    edge_image = Image.fromarray(edge_array, mode="L")

    details = {
        "device": str(selected_device),
        "width": original_gray.width,
        "height": original_gray.height,
        "processing_time": processing_time,
    }

    return original_gray, edge_image, details


def available_device():
    """Return CUDA when available; otherwise return CPU."""
    return "cuda" if torch.cuda.is_available() else "cpu"
