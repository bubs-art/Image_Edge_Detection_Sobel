import base64
from pathlib import Path
from io import BytesIO

import streamlit as st
from PIL import Image

from backend import detect_edges, available_device

st.set_page_config(
    page_title="Image Edge Detection | GPU Studio",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSET_PATH = Path(__file__).parent / "gpu_card.png"
GPU_IMAGE = base64.b64encode(ASSET_PATH.read_bytes()).decode("ascii") if ASSET_PATH.exists() else ""

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
    :root {{
      --bg:#08060d; --panel:#140d1c; --panel2:#1d1028; --purple:#a83cc7;
      --magenta:#e044d5; --pink:#f15ce8; --text:#faf6fc; --muted:#c0b2c9;
      --line:rgba(202,91,232,.42);
    }}
    html, body, [data-testid="stAppViewContainer"] {{
      background:#08060d; color:var(--text); font-family:'DM Sans',sans-serif;
    }}
    [data-testid="stAppViewContainer"] {{
      background:linear-gradient(180deg,rgba(5,3,10,.34),rgba(10,4,18,.56) 48%,rgba(5,3,10,.72));
      position:relative;
    }}
    [data-testid="stApp"] {{background:#08060d;}}
    .gpu-page-bg {{position:fixed;inset:0;z-index:-1;pointer-events:none;display:flex;align-items:center;justify-content:flex-end;
      overflow:hidden;opacity:.50;}}
    .gpu-page-bg img {{width:min(94vw,1500px);height:100vh;max-height:100vh;object-fit:contain;object-position:right center;
      mix-blend-mode:screen;filter:drop-shadow(0 0 36px rgba(194,42,239,.38));transform-origin:50% 50%;
      animation:gpu-scroll-spin linear both;animation-timeline:scroll(root block);animation-range:0% 100%;}}
    /* Positive rotateZ values make the full-page GPU wallpaper turn clockwise as scroll progress increases. */
    @keyframes gpu-scroll-spin {{from {{transform:rotateZ(0deg) scale(1);}}
      to {{transform:rotateZ(360deg) scale(1);}}}}
    .main,.block-container {{position:relative;z-index:1;}}
    .block-container {{isolation:isolate;}}
    [data-testid="stSidebar"] {{position:relative;z-index:2;}}
    [data-testid="stHeader"] {{background:transparent;}}
    .block-container {{max-width:1240px;padding-top:1.3rem;padding-bottom:3rem;}}
    #MainMenu, footer {{visibility:hidden;}}

    .topline {{display:flex;align-items:center;justify-content:space-between;margin:0 0 1.1rem;padding:.25rem .2rem;}}
    .brand {{display:flex;align-items:center;gap:.65rem;font-weight:800;letter-spacing:.02em;color:#fff;font-size:1.08rem;}}
    .brand-mark {{width:34px;height:34px;display:grid;place-items:center;border:1px solid #d64ce7;border-radius:11px;
      color:#f05bfa;box-shadow:0 0 22px #a82cc655;background:linear-gradient(145deg,#351044,#120a19);font-size:1.1rem;}}
    .brand small {{display:block;color:#bd9ac9;font-size:.62rem;letter-spacing:.2em;font-weight:600;margin-top:-2px;}}

    .hero {{position:relative;isolation:isolate;overflow:hidden;min-height:420px;padding:3.1rem 3rem 2.6rem;
      border:1px solid rgba(210,91,239,.30);border-radius:27px;margin:.2rem 0 2.1rem;
      background:linear-gradient(105deg,rgba(7,4,12,.82) 0%,rgba(12,6,19,.56) 54%,rgba(18,7,27,.20) 100%);
      box-shadow:0 22px 75px rgba(0,0,0,.24),inset 0 0 50px rgba(173,54,202,.04);}}
    .hero-copy {{position:relative;z-index:2;max-width:54%;}}
    .eyebrow {{display:inline-flex;align-items:center;gap:.5rem;border:1px solid rgba(214,82,238,.48);border-radius:99px;
      padding:.48rem .85rem;color:#e9b7f5;background:rgba(42,17,54,.6);font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;font-weight:700;margin-bottom:1.25rem;}}
    .hero h1 {{font-size:clamp(2.5rem,5.2vw,4.4rem);line-height:.99;letter-spacing:-.045em;margin:0 0 1.1rem;color:#fff;font-weight:800;}}
    .hero h1 span {{background:linear-gradient(95deg,#b83de2,#f34edb 70%,#ff8af0);-webkit-background-clip:text;background-clip:text;color:transparent;}}
    .hero p {{font-size:1.02rem;line-height:1.75;color:#d3c4dc;max-width:510px;margin:0 0 1.45rem;}}
    .hero-pills {{display:flex;flex-wrap:wrap;gap:.55rem;}}
    .hero-pill {{border:1px solid rgba(209,95,231,.32);background:rgba(28,14,39,.7);border-radius:99px;padding:.48rem .75rem;color:#d9c6e1;font-size:.75rem;}}
    .scroll-hint {{position:absolute;right:2rem;bottom:1.3rem;color:#e2b5ef;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;z-index:3;
      text-shadow:0 0 16px #a82bd0;}}

    .section-kicker {{color:#e7a0f1;text-transform:uppercase;letter-spacing:.22em;font-size:.68rem;font-weight:800;text-align:center;margin:2rem 0 .45rem;}}
    .section-heading {{font-size:1.9rem;font-weight:800;text-align:center;color:#fff;margin:0 0 .45rem;letter-spacing:-.03em;}}
    .section-heading span {{color:#d34de3;}}
    .section-sub {{color:var(--muted);text-align:center;margin:0 auto 1.45rem;max-width:650px;font-size:.92rem;}}

    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) {{position:relative;margin-top:1.35rem;padding-top:.8rem;
      border:1px solid rgba(210,77,237,.65)!important;border-radius:23px!important;background:linear-gradient(135deg,rgba(28,15,39,.97),rgba(12,9,18,.98))!important;
      box-shadow:0 0 38px rgba(161,42,198,.13),inset 0 0 30px rgba(176,56,207,.06);}}
    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]):before {{content:'▦  GPU MODULE';position:absolute;top:-13px;left:26px;padding:.32rem .75rem;border:1px solid #d04be5;border-radius:8px;
      color:#f1b4fa;background:#1b0d25;font-size:.66rem;letter-spacing:.16em;font-weight:800;box-shadow:0 0 20px #b93cda44;z-index:5;}}
    .panel-head {{display:flex;align-items:center;gap:.8rem;margin:.25rem 0 1rem;}}
    .chip-icon {{width:43px;height:43px;display:grid;place-items:center;border-radius:13px;color:#f15bfa;font-size:1.45rem;
      background:linear-gradient(145deg,#391348,#170c20);border:1px solid #b83bd0;box-shadow:0 0 20px #b83bd044;}}
    .panel-head h2 {{font-size:1.25rem;color:#fff;margin:0;font-weight:800;}}
    .panel-head p {{font-size:.8rem;color:#bfaec9;margin:.15rem 0 0;}}

    [data-testid="stFileUploader"] {{background:rgba(28,16,39,.8);border:1px dashed rgba(220,91,239,.78);border-radius:16px;padding:1rem;}}
    [data-testid="stFileUploader"] section {{background:transparent;}}
    [data-testid="stFileUploader"] small,[data-testid="stFileUploader"] label {{color:#eadcf0!important;}}
    [data-testid="stFileUploader"] button {{color:white!important;background:linear-gradient(100deg,#76278f,#b43bc0)!important;border:1px solid #d15add!important;border-radius:9px!important;}}
    [data-testid="stVerticalBlockBorderWrapper"] {{background:rgba(22,14,30,.84);border:1px solid rgba(198,105,220,.28);border-radius:17px;}}
    [data-testid="stMetric"] {{background:linear-gradient(145deg,#21152a,#17101e);border:1px solid var(--line);border-radius:14px;padding:1rem;}}
    [data-testid="stMetricLabel"] {{color:#c7b5ce!important;}} [data-testid="stMetricValue"] {{color:#f4d9fa!important;}}
    .stButton button,.stDownloadButton button {{background:linear-gradient(100deg,#76278f,#c13ac5)!important;color:white!important;border:1px solid #d85de5!important;
      border-radius:11px!important;font-weight:800!important;padding:.62rem 1.15rem!important;box-shadow:0 5px 22px #a12bbd38;transition:all .22s ease;}}
    .stButton button:hover,.stDownloadButton button:hover {{background:linear-gradient(100deg,#9634ae,#e044d5)!important;border-color:#f2a0f4!important;transform:translateY(-2px);box-shadow:0 8px 28px #c33cda55;}}
    [data-testid="stAlert"] {{background:#21152a;border:1px solid var(--line);color:#f7effa;}}
    [data-testid="stCaptionContainer"] {{color:#ad9ab7;}}
    h1,h2,h3,p,label {{font-family:'DM Sans',sans-serif;}} h2,h3 {{color:#f3e8f6!important;}}
    hr {{border-color:rgba(198,105,220,.22);}}
    @media(max-width:800px) {{.hero {{padding:2rem 1.4rem 5rem;min-height:440px;}}.hero-copy {{max-width:100%;}}
      .gpu-page-bg {{justify-content:center;opacity:.50;}}.gpu-page-bg img {{width:125vw;object-position:center;}}
      .scroll-hint {{right:1rem;}}}}
    @media(prefers-reduced-motion:reduce) {{.gpu-page-bg img {{animation:none!important;}}}}
    </style>
    {f'<div class="gpu-page-bg"><img src="data:image/png;base64,{GPU_IMAGE}" alt="GPU background"></div>' if GPU_IMAGE else ''}
    <div class="topline">
      <div class="brand"><div class="brand-mark">⌁</div><div>EdgeDetect<small>GPU COMPUTE STUDIO</small></div></div>
      <div style="color:#c9b7d2;font-size:.78rem;letter-spacing:.08em">COMPUTER VISION&nbsp;&nbsp; / &nbsp;&nbsp;SOBEL FILTER</div>
    </div>
    <section class="hero">
      <div class="hero-copy">
        <div class="eyebrow">⚡ AI-powered computer vision</div>
        <h1>Image Edge<br><span>Detection</span></h1>
        <p>Reveal the details hidden in every image. Explore Sobel edge detection with PyTorch and GPU-accelerated processing.</p>
        <div class="hero-pills"><span class="hero-pill">✦ PyTorch powered</span><span class="hero-pill">▣ CPU / CUDA</span><span class="hero-pill">◈ Real-time results</span></div>
      </div>
      <div class="scroll-hint">↓ &nbsp; Scroll to rotate GPU</div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🟣 Project details")
    st.write("**Algorithm:** Sobel Edge Detection")
    st.write("**Backend:** Python + PyTorch")
    st.write("**Frontend:** Streamlit")
    st.write("**Processing:** CPU / CUDA GPU")
    st.divider()
    st.caption("The image is converted to grayscale. Sobel X and Sobel Y filters are applied, and their combined magnitude forms the edge image.")

with st.container(border=True):
    st.markdown(
        '<div class="panel-head"><div class="chip-icon">▦</div><div><h2>Image Edge Detection</h2><p>Upload your image and let the Sobel filter reveal its edges.</p></div></div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
        help="Upload a clear image to see its edges.",
    )

if uploaded_file is not None:
    try:
        input_image = Image.open(uploaded_file)
        device = available_device()
        original, edges, details = detect_edges(input_image, device)

        st.success("Edge detection completed successfully!")
        st.markdown('<div class="section-kicker">Your output</div><div class="section-heading">Original <span>vs detected edges</span></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            with st.container(border=True):
                st.subheader("🖼️ Original image")
                st.image(original, use_container_width=True)
                st.caption("Converted to grayscale before processing")
        with col2:
            with st.container(border=True):
                st.subheader("✧ Detected edges · Sobel")
                st.image(edges, use_container_width=True)
                st.caption("Combined horizontal and vertical edge response")

        st.markdown('<div class="section-kicker">System telemetry</div><div class="section-heading">Processing <span>information</span></div>', unsafe_allow_html=True)
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Image width", f'{details["width"]} px')
        metric2.metric("Image height", f'{details["height"]} px')
        metric3.metric("Processing time", f'{details["processing_time"]:.6f} s')
        st.caption(f'▣ Compute device: {details["device"]}')

        output_buffer = BytesIO()
        edges.save(output_buffer, format="PNG")
        st.download_button(
            label="⬇  Download edge-detected image",
            data=output_buffer.getvalue(),
            file_name="edge_detected_output.png",
            mime="image/png",
        )
    except Exception as error:
        st.error(f"Could not process this image: {error}")
else:
    with st.container(border=True):
        st.markdown("### ✦ Ready when you are")
        st.markdown("1. Click **Browse files** and select a JPG or PNG image.\n2. The app converts the image to grayscale.\n3. View the original image and its Sobel edge map.\n4. Download the processed result.")

st.divider()
st.markdown('<div style="text-align:center;color:#a98bb7;font-size:.72rem;letter-spacing:.17em;padding:.5rem">MINI PROJECT &nbsp; / &nbsp; IMAGE EDGE DETECTION USING SOBEL FILTER AND PYTORCH</div>', unsafe_allow_html=True)
