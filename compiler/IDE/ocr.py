# if tesseract is not in environment variables

def ocr_core(filename):
    from PIL import Image
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = r'D:\Live Softwares\Tesseract-OCR\tesseract.exe'
    """
    This function will handle the core OCR processing of images.
    """
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    text = pytesseract.image_to_string(Image.open(filename))
    return text