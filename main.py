""" 

"""

import os
import sys
import time
from PIL import Image

import easyocr
import streamlit as st

# sys.path.append("./src")
from src.logger import get_logger
from src.Config import Config
from src.Invoice import Invoice
from src.PredictionService import PredictionService


if "logger" not in st.session_state:
    st.session_state.logger = get_logger()

if "config" not in st.session_state:
    st.session_state.config = Config(logger=st.session_state.logger)

if "invoice" not in st.session_state:
    st.session_state.invoice = Invoice(logger=st.session_state.logger)

@st.cache_resource
def load_detection_model():
    """
    """
    return PredictionService(logger=st.session_state.logger)

@st.cache_resource
def load_ocr_model():
    """
    """
    return easyocr.Reader(['en'])


detection_model = load_detection_model()
ocr_model = load_ocr_model()

def get_roi(uploaded_images: list) -> None:
    """ 
    Method Docstring not implemented yet
    """
    #Delete old files
    for file in os.listdir("src/temp/"):
        os.remove(f"src/temp/{file}")

    for idx, file in enumerate(uploaded_images):
        img = Image.open(file)
        img = img.save(f"src/temp/img_{idx}.jpg")

    if uploaded_images is not None:
        start_time = time.time()
        for img in os.listdir(f"{st.session_state.config.folder_src()}/temp/"):
            detection_model.extract_table(
                img=f"{st.session_state.config.folder_src()}/temp/{img}", confidence=0.7
                )

        end_time = time.time()
        st.session_state.logger.info(
            f"Images were detected and extracted in {end_time-start_time} sec."
            )

def get_total_price() -> float:
    """ 
    Method Docstring not implemented yet
    """
    start_time = time.time()

    total: float = 0
    for img in os.listdir(f"{st.session_state.config.folder_src()}/temp/"):
        if str(img).startswith("price"):
            total_part = detection_model.extract_text(
                img=img,
                reader=ocr_model
                )
            total += total_part

    end_time = time.time()
    st.session_state.logger.info(f"Total price was calculated in {end_time-start_time} sec.")
    return round(total, 2)

def write_invoice(paypal_email, hourly_rate, hours_worked) -> None:
    """ 
    Method Docstring not implemented yet
    """
    st.session_state.invoice.write_image(
        total=get_total_price(),
        paypal_email=paypal_email,
        hourly_rate=hourly_rate,
        hours_worked=hours_worked
        )


# -------Streamlit------- #
def main() -> None:
    """ 
    Method Docstring not implemented yet
    """
    finished = False
    st.header('Rechnung erstellen', divider="grey")

    paypal_email = st.text_input(
        "PayPal E-Mail"
    )

    hourly_wage = st.number_input(
        "Stundenlohn (Euro)", min_value=10.0, step=0.5, format="%.2f"
        )
    time_worked = st.number_input(
        "Gearbeitete Zeit (Stunden)", min_value=0.0, step=0.5, format="%.1f"
        )

    with st.form("my-form", clear_on_submit=True):
        uploaded_images = st.file_uploader(
            "Rechnungen auswählen", type=["jpg", "jpeg", "png"], accept_multiple_files=True
            )

        submitted = st.form_submit_button("Upload files!")

        if len(uploaded_images) > 0 and submitted:
            with st.spinner("Wait for it ..."):
                get_roi(uploaded_images=uploaded_images)
                write_invoice(
                    paypal_email=paypal_email,
                    hourly_rate=hourly_wage,
                    hours_worked=time_worked
                    )
            st.success("Done!")
            finished = True

    if finished is True:
        with open("invoice_final.pdf", 'rb') as f:
            st.download_button("Download Invoice", f, file_name="invoice_final.pdf")
        finished = False


if __name__ == '__main__':
    main()
