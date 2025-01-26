# PDFextract

This project is a full-stack application utilizing Next.js for the frontend and Flask for the backend.
The web-app accepts a PDF file and a [Mistral AI api key](https://console.mistral.ai/api-keys/).

It then allows the user to view the extracted text, the metadata of the file uploaded. It also allows the user to chat to an LLM and ask anything regarding the text from the submitted pdf to it. 

## Project Structure

```
PDFextract
├── frontend          # Next.js frontend application
│   ├── pages        # Contains the pages of the application
│   ├── styles       # Global CSS styles
│   ├── package.json # npm configuration and dependencies
│   └── next.config.js # Next.js configuration
├── backend           # Flask backend application
|   ├── modules       # modules folder containing the functionalities
|   |   ├── __init__.py  # init file
|   |   ├── llm.py        # file containing llm api connection
|   |   └── pdfextractor.py # pdf extraction logic
│   ├── app.py       # Main entry point for the Flask app
│   ├── requirements.txt # Python dependencies for Flask
│   └── wsgi.py      # WSGI server entry point
├── vercel.json      # Vercel deployment configuration
└── README.md        # Project documentation
```

