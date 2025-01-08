import streamlit as st
import requests
from PIL import Image
import io
import base64

# Function to analyze the image using the Imagga API
def analyze_image(image, api_key, api_url):
    api_key="acc_a223593f59eb3ca"
    api_url="https://api.imagga.com/v2"
    
    if image.mode == 'RGBA': image = image.convert('RGB')
    # Convert the image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    headers = {
        'Authorization': f'Basic {api_key}',
    }
    data = {
        'image_base64': img_str,
    }
    response = requests.post(api_url, headers=headers, data=data)
    return response.json()

# Function to display patient history and vitals form
def get_patient_info():
    st.subheader("Patient History and Vitals")
    
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    sex = st.selectbox("Sex", ("Male", "Female", "Other"))
    
    st.subheader("Medical History")
    medical_history = st.text_area("Medical History")
    
    st.subheader("Specific Disease Information")
    disease_info = {}
    diseases = ["Disease1", "Disease2", "Disease3"]  # Add your specific diseases here
    for disease in diseases:
        disease_info[disease] = st.text_area(f"History for {disease}")
    
    st.subheader("Vitals")
    height = st.number_input("Height (cm)", min_value=0.0)
    weight = st.number_input("Weight (kg)", min_value=0.0)
    blood_pressure = st.text_input("Blood Pressure")
    pulse = st.number_input("Pulse", min_value=0)
    spo2_levels = st.number_input("SpO2 Levels", min_value=0)
    
    return {
        "name": name,
        "age": age,
        "sex": sex,
        "medical_history": medical_history,
        "disease_info": disease_info,
        "vitals": {
            "height": height,
            "weight": weight,
            "blood_pressure": blood_pressure,
            "pulse": pulse,
            "spo2_levels": spo2_levels
        }
    }

# Streamlit app
st.title("Eye Infection Detection App")
st.write("Upload a fundus image and provide patient information to detect eye infections.")

api_key = st.text_input("Imagga API Key")
api_url = st.text_input("Imagga API Endpoint", "https://api.imagga.com/v2/tags")

uploaded_image = st.file_uploader("Upload Fundus Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Fundus Image", use_container_width=True)

    patient_info = get_patient_info()

    if st.button("Analyze"):
        result = analyze_image(image, api_key, api_url)
        st.write("Analysis Result:", result)
        st.write("Patient Information:", patient_info)
