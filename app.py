import streamlit as st
from utils import extract_text_from_pdf, summarize_text

st.set_page_config(page_title="StudyMate", layout="wide", page_icon="📚")

# Custom CSS for better appearance
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #9D7FEA;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #7B5FC7;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyMate - Your Smart PDF Study Buddy")
st.markdown("Upload your textbook or notes and get AI-powered summaries instantly!")

# Sidebar with instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload** your PDF file
    2. Click **Extract & Summarize**
    3. View the extracted text and summary
    
    ### 💡 Tips:
    - Works best with text-based PDFs
    - Scanned documents may not work
    - Longer documents = better summaries
    """)
    
    st.header("⚙️ Settings")
    sentence_count = st.slider("Summary Length (sentences)", 3, 10, 5)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your textbook or notes (PDF)", 
        type=["pdf"],
        help="Choose a PDF file from your computer"
    )

with col2:
    if uploaded_file:
        st.success("✅ PDF uploaded successfully!")
        st.info(f"📄 File: {uploaded_file.name}")
        st.info(f"📦 Size: {uploaded_file.size / 1024:.2f} KB")

if uploaded_file:
    if st.button("🚀 Extract & Summarize", use_container_width=True):
        
        # Create tabs for better organization
        tab1, tab2 = st.tabs(["📄 Extracted Text", "🧠 Summary"])
        
        with tab1:
            with st.spinner("Extracting text from PDF..."):
                text = extract_text_from_pdf(uploaded_file)
                
                if text.startswith("⚠️") or text.startswith("❌"):
                    st.error(text)
                else:
                    st.subheader("📄 Extracted Text")
                    
                    # Show word count
                    word_count = len(text.split())
                    st.info(f"📊 Total words extracted: {word_count}")
                    
                    # Show preview in expandable section
                    with st.expander("🔍 View first 1000 characters", expanded=True):
                        st.text(text[:1000])
                    
                    # Option to view full text
                    with st.expander("📖 View full text"):
                        st.text(text)
                    
                    # Download option
                    st.download_button(
                        label="💾 Download extracted text",
                        data=text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
        
        with tab2:
            with st.spinner("Generating summary..."):
                if not (text.startswith("⚠️") or text.startswith("❌")):
                    summary = summarize_text(text, sentence_count)
                    
                    st.subheader("🧠 AI-Generated Summary")
                    
                    if summary.startswith("⚠️") or summary.startswith("❌"):
                        st.warning(summary)
                    else:
                        # Show summary in a nice box
                        st.markdown(f"""
                        <div style="background-color: #F5F2FF; padding: 20px; border-radius: 10px; border-left: 5px solid #9D7FEA;">
                        {summary}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download summary
                        st.download_button(
                            label="💾 Download summary",
                            data=summary,
                            file_name="summary.txt",
                            mime="text/plain"
                        )
                        
                        # Show statistics
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Original Length", f"{len(text.split())} words")
                        with col_b:
                            st.metric("Summary Length", f"{len(summary.split())} words")
                else:
                    st.error("Cannot generate summary due to text extraction error.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Made with ❤️ by Madina Karishma | StudyMate v2.0</p>
</div>
""", unsafe_allow_html=True)
