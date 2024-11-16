# Pdf-readerr
How It Works

1. File Selection: The app uses a FileChooserListView to allow you to select a PDF file from your device.


2. PDF Rendering: The script uses PyMuPDF (fitz) to render each PDF page as an image.


3. Navigation: Navigate through pages using "Previous" and "Next" buttons.


4. Error Handling: Displays a popup if the PDF fails to load.




---

Features

Loads and displays PDF files.

Allows navigation between pages.

Shows the current page number and total pages.



---

Run the App

Run the app using:

python pdf_reader.py


---

Notes

The app displays one page at a time.

Temporary image files (temp_page.png) are generated for each page to display on the Kivy Image widget.

You can enhance this with more features like zooming or text search.
