import pdfplumber

# Open the PDF file and extract text from each page
with pdfplumber.open("Dataset\Job_description_DS.pdf") as pdf:
    # Extract text from each page 
    for page in pdf.pages:
        text = page.extract_text()
        print(text)



