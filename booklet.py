try:
    from pypdf import PdfFileReader, PdfFileWriter
    from pypdf.pdf import PageObject
    from pypdf.generic import RectangleObject
except:
    print(
        "please install PyPDF4 with pip install git+https://github.com/claird/PyPDF4.git@fc6cf15c736332248783158241206946eff94899"
    )
    quit()

import argparse
from math import ceil, floor
from typing import List, Generator, Any
from pathlib import Path

class Args:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="generate bookleted pdf")
        self.addArguments()

    def addArguments(self) -> None:
        self.parser.add_argument(dest="docPath", type=Path, help="path of input pdf")
        self.parser.add_argument(
            "-o", "--out", type=Path, dest="outPath", help="output path of the file"
        )
        self.args = self.parser.parse_args()

    @property
    def docPath(self) -> str:
        return str(self.args.docPath.absolute())

    @property
    def outPath(self) -> Any:
        return str(self.args.outPath.absolute()) if self.args.outPath else None


class Booklet:
    def __init__(self, args: Args, str="booklet.pdf", bind: str = "left") -> None:

        self.doc = PdfFileReader(args.docPath)
        self.numPages = self.doc.numPages
        assert (
            not self.numPages % 4
        ), "your source pdf must have number of pages divisible by 4"
        outPath = args.outPath if args.outPath else "booklet.pdf"
        self.writer = PdfFileWriter(outPath)
        self.bind = bind

    def yieldSequence(self) -> Generator[List[int], None, None]:
        for i in range(0, self.numPages // 2):
            currentPage = [self.numPages // 2 - i - 1, self.numPages // 2 + i]
            if self.bind == "right" and not i % 2:
                currentPage = currentPage[::-1]
            if i % 2 and self.bind != "right":
                currentPage = currentPage[::-1]
            yield currentPage

    def makeBooklet(self) -> None:
        for spread in self.yieldSequence():
            print(f"processing {spread}")
            width: List[int]
            height: List[int]
            width, height = [], []
            for i, pageNum in enumerate(spread):
                width.append(self.doc.getPage(pageNum).mediaBox.getWidth())
                height.append(self.doc.getPage(pageNum).mediaBox.getHeight())
            sheet = PageObject.createBlankPage(None, sum(width), max(height))
            for i, pageNum in enumerate(spread):
                shift = 0 if i == 0 else width[i - 1]
                page = self.doc.getPage(pageNum)
                sheet.mergeScaledTranslatedPage(page, 1, shift, 0)
            self.writer.addPage(sheet)

    def writeBooklet(self) -> None:
        self.writer.write()
        print("booklet is done")

if __name__ == "__main__":

    args = Args()
    booklet = Booklet(args)
    booklet.makeBooklet()
    booklet.writeBooklet()
