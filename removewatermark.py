import fitz
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def remove_watermark_image(src, dst, width=963, height=215):
    doc = fitz.open(src)
    change = False
    for page in range(doc.pageCount):
        images = doc.getPageImageList(page)
        for content in doc[page].getContents():
            c = doc.xrefStream(content)
            for _, _, wh, ht, _, _, _, img, _ in images:
                if wh == width and ht == height:
                    c = c.replace("/{} Do".format(img).encode(), b"")
                    change = True
            doc.updateStream(content, c)

    if change == True:
        doc.save(dst)   
    return change

def remove_watermark_words(src, dst, words):
    doc = fitz.open(src)
    change = False
    
    for n in range(doc.pageCount):
        times = 0
        #print(doc[n].getContents())
        while words in doc[n].getText():
            #print(doc[n].getText())
            if n == 0 and times > 3:
                print("去除水印失败：" + os.path.basename(src))
                break
            elif n == 0 and times > 0:
                print("第 %s 次去水印：%s" % (str(times+1), os.path.basename(src)))
            cont = doc[n].getContents()[-1-times]
            doc.updateStream(cont,b" ")
            times += 1
            change = True

    if change == True:
        doc.save(dst) 

    return change

def remove_word_mark(input_fname: str, output_fname: str):

    with open(input_fname, "rb") as inputFile:
        reader = PdfFileReader(inputFile)
        writer = PdfFileWriter()

        for n in range(reader.numPages):
            page = reader.getPage(n)
            del page["/Contents"][-1]
            writer.addPage(page)

        dirDst = os.path.dirname(output_fname)
        if not os.path.exists(dirDst):
        	os.makedirs(dirDst) 
        writer.write(open(output_fname, "wb") )

def remove_watermark_words_ex(src, dst, words):
	change = False
	filename = src
	nums = 0;
	while True:
		if not os.path.exists(filename):
			break
		if nums > 3:
			print("去除水印失败：" + src)
			break
		doc = fitz.open(filename)
		txt = doc[0].getText()
		#print(txt)
		if words in txt:
			if nums > 0:
				print("第 %s 次去水印：%s" % (str(nums+1), src))
				dst = os.path.join(os.path.dirname(dst), "times%s" % (nums+1), os.path.basename(dst))
			remove_word_mark(filename, dst)
			filename = dst
			nums += 1;
		else:
			if nums > 0:
				change = True
			break
	return change