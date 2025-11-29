import streamlit as st
import requests
import PyPDF2
import docx

st.set_page_config(page_title="AI Dokument Asistent", page_icon="🤖", layout="wide")

# ----------------------------------------------------
# 1. API KLJUČ IN URL
# ----------------------------------------------------
API_KEY = st.secrets["API_KEY"]
API_URL = st.secrets["API_URL"]

# ----------------------------------------------------
# 2. FUNKCIJA ZA KLIC MODEL-A
# ----------------------------------------------------
def ask_model(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "llama3.2",
        "prompt": prompt
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return f"Napaka: {response.status_code}\n{response.text}"

# ----------------------------------------------------
# 3. FUNKCIJE ZA BRANJE DOKUMENTOV
# ----------------------------------------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_docx(file):
    document = docx.Document(file)
    return "\n".join([p.text for p in document.paragraphs])

# ----------------------------------------------------
# 4. UI
# ----------------------------------------------------
st.title("🤖 AI Dokument Asistent – Napredna verzija")

st.subheader("📄 Uvozi dokument (PDF, DOCX) ali vpiši vprašanje")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Naloži dokument:", type=["pdf", "docx"])

with col2:
    user_question = st.text_area("Vnesi vprašanje ali besedilo:")

if st.button("🔍 Analiziraj"):
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type == "pdf":
            content = read_pdf(uploaded_file)
        elif file_type == "docx":
            content = read_docx(uploaded_file)
        else:
            st.error("Nepodprt format.")
            st.stop()

        st.info("Dokument uspešno prebran. Pošiljam modelu…")

        answer = ask_model(f"Tu je dokument:\n{content}\n\nUporabnikovo vprašanje:\n{user_question}")
        st.success("Odgovor:")
        st.write(answer)

    elif user_question.strip():
        st.info("Pošiljam vprašanje modelu…")
        answer = ask_model(user_question)
        st.success("Odgovor:")
        st.write(answer)
    else:
        st.warning("Vnesi vsaj besedilo ali naloži dokument.")
