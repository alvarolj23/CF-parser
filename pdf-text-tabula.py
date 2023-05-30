import tabula
def extract_tables(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables

def process_table(table):
    # Perform any necessary processing on the table
    # This can include data cleaning, filtering, restructuring, etc.
    processed_table = table  # Placeholder, modify as per your requirements
    return processed_table

def extract_resume_data(pdf_path):
    tables = extract_tables(pdf_path)
    processed_tables = []
    
    for table in tables:
        processed_table = process_table(table)
        processed_tables.append(processed_table)
    
    # Perform further analysis or extraction on the processed tables
    
    return processed_tables

#extract the text from the pdf
pdf= extract_resume_data("CF_Alvaro_MARIA.pdf")

print(pdf)
#write the text to a file
#file = open("CF_txt_tabula.txt", "w")
#file.write("\n\n".join(pdf))
#file.close()