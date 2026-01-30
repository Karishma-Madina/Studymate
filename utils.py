import fitz
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import os

# Download NLTK data with better error handling
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)  # New version requirement

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        # Open PDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text.strip():  # Only add non-empty pages
                text += page_text + "\n"
        
        doc.close()
        
        # Check if text was extracted
        if not text.strip():
            return "⚠️ No text could be extracted from this PDF. It might be an image-based PDF or scanned document."
        
        return text.strip()
    
    except Exception as e:
        return f"❌ Error extracting text: {str(e)}"

def summarize_text(text, sentence_count=5):
    """Summarize text using TextRank algorithm"""
    try:
        # Check if text is too short
        if len(text.split()) < 50:
            return "⚠️ Text is too short to summarize meaningfully. Need at least 50 words."
        
        # Check if text is an error message
        if text.startswith("⚠️") or text.startswith("❌"):
            return text
        
        # Parse and summarize
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        
        # Adjust sentence count based on document length
        actual_sentence_count = min(sentence_count, len(text.split('.')) - 1)
        actual_sentence_count = max(1, actual_sentence_count)  # At least 1 sentence
        
        summary = summarizer(parser.document, actual_sentence_count)
        
        if not summary:
            return "⚠️ Could not generate summary. The text might be too short or lack meaningful content."
        
        return " ".join(str(sentence) for sentence in summary)
    
    except Exception as e:
        return f"❌ Error during summarization: {str(e)}\n\nTry uploading a different PDF or check if the document has enough readable text."
