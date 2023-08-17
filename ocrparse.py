import pytesseract
from pdf2image import convert_from_path
import os
from PyPDF2 import PdfWriter, PdfReader, PdfFileMerger
import io
import sys
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# print("HEREEE")
def convert_pdf_to_searchable_pdf(pdf_path, output_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    try:
    # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        merger = PdfFileMerger()
        # Create a list to store image bytes for each page
        image_bytes_list = []
        for image in images:
            # Perform OCR on the image and get the text (without writing to a file)
            text = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
            image_bytes_list.append(text)       
        # print("made it here")
        # Create a new searchable PDF by combining the OCR output from all pages
        with open(output_path, 'wb') as f:
            for image_bytes in image_bytes_list:
                pdf_reader = PdfReader(io.BytesIO(image_bytes))
                page = pdf_reader.pages[0]
                page.scale(0.5, 0.5) #page.scale(zoom_factor_x, zoom_factor_y)
                merger.append(pdf_reader)
                # pdf_writer.add_page(PdfReader(io.BytesIO(image_bytes)).pages[0])
            # pdf_writer.write(f)
            merger.write(f)

        print("Searchable PDF created successfully.")
    except Exception as e:
        print("Error: ", e)
        print("File: ", pdf_path)

if __name__ == "__main__":
    OUTPUT_DIRECTORY = "./Output/"
    file = sys.argv[1]
    # print("HEEREE")
    convert_pdf_to_searchable_pdf(file, OUTPUT_DIRECTORY + file[:-4] + "_processed.pdf")

