import pdftotext

# Load your PDF
with open("CF_Alvaro_MARIA.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)


# How many pages?
print(len(pdf))

# Iterate over all the pages
for page in pdf:
    print(page)

# Read some individual pages
print(pdf[0])
print(pdf[1])

# Read all the text into one string
#print("\n\n".join(pdf))

file = open("CF_txt.txt", "w")
file.write("\n\n".join(pdf))
file.close()