#!/bin/bash

pdfimages -all mpdf.pdf ./

python -c 'from PIL import Image
im = Image.open("-000.png")
data=b"".join(map(lambda d: bytes(d)[::-1], im.getdata()))[4:].replace(b"\x00", b"")
open("out.txt","wb").write(data)'

rm -f -- *.pdf *png
