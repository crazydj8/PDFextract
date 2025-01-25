import fitz  # PyMuPDF

class PDFextractor():
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file_stream, preserve_layout=False):
        # Initialize an empty dictionary to store text by page
        pdf_text = {}
        
        try:
            # Open the PDF document
            doc = fitz.open(stream=file_stream, filetype="pdf")
            
            # Iterate through all pages
            for page_num in range(len(doc)):
                # Get the page
                page = doc[page_num]
                
                # Extract text based on layout preservation setting
                if preserve_layout:
                    # Blocks preserves more of the original layout
                    text_blocks = page.get_text("blocks")
                    page_text = "\n".join([block[4] for block in text_blocks if block[4].strip()])
                else:
                    # Simple text extraction
                    page_text = page.get_text().strip()
                
                # Only add non-empty pages to the dictionary
                if page_text:
                    pdf_text[page_num + 1] = page_text
            
            # Close the document
            doc.close()
        
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
            return {}
        
        return pdf_text

    def extract_pdf_metadata(self, file_stream):
        try:
            doc = fitz.open(stream=file_stream, filetype="pdf")
            metadata = doc.metadata
            doc.close()
            return metadata
        except Exception as e:
            print(f"An error occurred while extracting metadata: {e}")
            return {}
        
    def extract_pdf_data(self, file_stream):
        metadata = self.extract_pdf_metadata(file_stream)
        pdf_text = self.extract_text_from_pdf(file_stream)
        resultjson = {"text_found": True if pdf_text else False,
                    "text": pdf_text,
                    "metadata": metadata
                    }
        
        return resultjson

pdf_extractor = PDFextractor()