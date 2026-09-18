import streamlit as st
import os
from PIL import Image
from similarity import search_bag

# Page configuration
st.set_page_config(page_title="Handbag Scanner", layout="centered")

st.title("Handbag Scanner")
st.markdown("Upload a bag image to find its reference in the database.")

# Upload widget
uploaded_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"], label_visibility="hidden")

if uploaded_file is not None:
    # Load user image
    user_img = Image.open(uploaded_file).convert('RGB')
    
    with st.spinner("Analyzing image..."):
        # Process image through our core function
        result = search_bag(user_img)
        
    if result:
        brand, model, price, img_file, distance = result[0]
        
        # Match logic based on threshold
        if distance <= 0.04:
            status = "Exact match"
        elif distance <= 0.09:
            status = "Similar model"
        else:
            status = "No exact match found"

        st.markdown("---")
        
        # Side-by-side layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Target Image**")
            st.image(user_img, use_container_width=True)
            st.markdown(f"*Distance Score: {distance:.4f}*")
            
        with col2:
            st.markdown(f"**Database Match: {status}**")
            
           # Extract only the exact filename, ignoring any folder path stored in DB
            file_name = os.path.basename(img_file)
            
            # Rebuild the exact local path
            db_img_path = os.path.join("..", "data", "images", file_name)
            
            if os.path.exists(db_img_path):
                db_img = Image.open(db_img_path)
                st.image(db_img, use_container_width=True)
            else:
                st.error("Physical image not found on disk.")
                st.write(f"**Searched path:** `{db_img_path}`")
            
            # Details
            st.markdown(f"**Brand:** {brand}")
            st.markdown(f"**Model:** {model}")
            st.markdown(f"**Price:** ~{price}")