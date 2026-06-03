import streamlit as st

from document_extractor import load_document
from text_splitter import split_text
from vector_store import create_vector_store
from rag_chain import create_rag_chain


# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Retrivara",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------
# Custom Styling
# ---------------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e3a8a 50%,
        #2563eb 100%
    );
}

/* Main Container */
.main > div {
    background-color: rgba(255,255,255,0.96);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
}

/* Title */
h1 {
    text-align: center;
    color: #1e3a8a !important;
}

/* Headers */
h2, h3 {
    color: #2563eb !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    border: 2px dashed #2563eb;
}

/* Text Input */
.stTextInput input {
    border-radius: 10px;
    border: 2px solid #2563eb;
}

/* Answer Box */
.answer-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-top: 10px;
}

/* Success Message */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Header
# ---------------------------------------
st.title("🔍 Retrivara")

st.markdown(
    """
    <h4 style='text-align:center;color:#64748b;'>
    Transforming Documents into Knowledge
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------
# Upload Section
# ---------------------------------------
st.subheader("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX file",
    type=["pdf", "docx"]
)

# ---------------------------------------
# Process Document
# ---------------------------------------
if uploaded_file:

    with st.spinner("Processing document..."):

        text = load_document(uploaded_file)

        chunks = split_text(text)

        vectorstore = create_vector_store(chunks)

        qa_chain = create_rag_chain(vectorstore)

    st.success("✅ Document processed successfully!")

    st.write(f"Document Length: {len(text)} characters")
    

    st.markdown("---")

    # ---------------------------------------
    # Question Section
    # ---------------------------------------
    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question about the document"
    )

    if question:

        with st.spinner("Generating answer..."):

            response = qa_chain.invoke(
                {"input": question}
            )

        st.subheader("📌 Answer")

        st.markdown(
            f"""
            <div class="answer-box">
            {response["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")

st.caption(
    "Retrivara • AI-Powered Document Question Answering System"
)