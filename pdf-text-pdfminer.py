from pdfminer.high_level import extract_text

def extract_plain_text(pdf_path):
    plain_text = extract_text(pdf_path)
    return plain_text

#extract the text from the pdf
pdf= extract_plain_text("CF_Alvaro_MARIA.pdf")

#write the text to a file
file = open("CF_txt_pdfminer.txt", "w")
file.write("\n\n".join(pdf))
file.close()