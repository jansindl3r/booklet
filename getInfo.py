from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
def rotate_odd(path, output):
    reader = PdfReader(path)
    writer = PdfWriter()
    pages = reader.pages
    
    for page in range(len(pages)):
        if page % 2:
            # pages[page].Crop = [0, 100, 300, 300]
            help(pages)
            
            writer.addpage(pages[page])
        
    writer.write(output)
    
if __name__ == '__main__':
    rotate_odd('bleed.pdf', 'out.pdf')