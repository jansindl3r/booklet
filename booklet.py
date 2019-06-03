from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
from math import ceil, floor

# change file_name
file_name = input('name of your pdf file')

if file_name.endswith('.pdf'):
	file_name = file_name[:file_name.rfind('.pdf')]

print(file_name)


file = PdfFileReader(open(file_name + '.pdf','rb'))
pages_count = len(file.pages)

pages = pages_count
if pages % 4 != 0:
    pages_count += 4 - pages_count % 4

print(pages, pages_count)

half = int(floor(pages_count/2))

sequences = []

for page in range(0, int(pages_count/2), 1):
	if page % 2 == 0:
		sequences.append([half - page, half + 1 + page])
	if page % 2 != 0:
		sequences.append([half + 1 + page, half - page])

print(sequences)
width = file.getPage(0).mediaBox.getWidth()
height = file.getPage(0).mediaBox.getHeight()

writer = PdfFileWriter()

for seq in sequences:
	print(seq)
	translated_page = PageObject.createBlankPage(None, width*2, height)

	if seq[0] > pages or seq[0] < 0:
		second_page = PageObject.createBlankPage(None, width, height)
	else:
		second_page = file.getPage(seq[0] - 1)

	if seq[1] > pages or seq[1] < 0:
		first_page = PageObject.createBlankPage(None, width, height)
	else:
		first_page = file.getPage(seq[1] - 1)

	
	translated_page.mergeScaledTranslatedPage(first_page, 1, width, 0)  # -400 is approximate mid-page

	translated_page.mergePage(second_page)

	writer.addPage(translated_page)

with open(file_name + '_booklet.pdf', 'wb') as f:
	writer.write(f)