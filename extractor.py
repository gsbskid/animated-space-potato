from tqdm.notebook import tqdm
from unstructured.partition.image import partition_image
import os 

import fitz 
import json

import PyPDF2

def extract_text_as_unstructured() : 

    pdfs = os.listdir('PDFs')
    pdfs = [f'PDFs/{pdf}' for pdf in pdfs]
    full_text = ''

    for pdf in tqdm(pdfs , total = len(pdfs)) : 

        pdf = f'PDFs/{pdf}'
        images = os.listdir(pdf)

        for image in tqdm(images , total = len(images)) : 

            image_path = f'{pdf}/{image}'
            elements = partition_image(image_path)

            for ele in elements : full_text += ele.text + '\n'

def extract_text_as_headings() : 

    def extract_headings_and_contents(pdf_paths) :
        '''
        Function to extract headings and contents from a PDF

        Args :
            1) pdf_paths : list : list of paths to PDFs
            2) red_color : int : red color to extract headings

        Returns :
            1) dict : headings and contents
        '''

        headings_contents = {}
        current_heading = None
        current_content = ''

        # Loop through the PDFs

        for path in pdf_paths : 

            # Open the PDF

            doc = fitz.open(path)

            for page in doc : 

                # Get the blocks

                blocks = page.get_text('dict')['blocks']

                for block in blocks :

                    # Get the lines

                    try :  

                        for line in block['lines'] : 

                            # Get the spans

                            try :

                                for span in line['spans'] : 

                                    # Extract the text

                                    try : 

                                        # Extract the color, text and size

                                        color = span['color']
                                        text = span['text']
                                        size = span['flags']

                                        # Check if the color is red or the size is bold, if so, then it is a heading

                                        if color == 14176347 or size & 1 << 5 : 

                                            # If there is a current heading, then add the content to the dictionary

                                            if current_heading : 

                                                # Add the content to the dictionary

                                                if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() + '\n' 
                                                else : headings_contents[current_heading] = current_content.strip()

                                            # Update the current heading and content

                                            current_heading = text
                                            current_content = ''

                                        else : current_content += text + ''

                                    except : pass
                            except : pass
                    except : pass

            # Add the last content to the dictionary

            if current_heading : 

                if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() 
                else : headings_contents[current_heading] = current_content.strip()

        return headings_contents

    sections = extract_headings_and_contents([
        'Assets/PDFs/input_pdf_20.pdf' , 
        'Assets/PDFs/pzuw- 1 column.pdf' , 
        'Assets/PDFs/SWU_WDCiR_2014_02 - 1 column.pdf'
    ])

    json_data = json.dumps(sections)

    with open('Assets/JSONs/data.json' , 'w') as fil : json.dump(json_data, fil)

def extract_full_text() : 

    def pdf_to_text(path) : 

        pdf_reader = PyPDF2.PdfReader(path)
        num_pages = len(pdf_reader.pages)

        text = ''

        for i in range(num_pages):
            page_object = pdf_reader.pages[i]
            text += page_object.extract_text()

        return text 

    pdfs = os.listdir('Assets/PDFs')
    full_text = ''

    pdfs = [
        f'Assets/PDFs/{pdf}'
        for pdf 
        in pdfs
    ]

    for pdf in tqdm(pdfs , total = len(pdfs)) : full_text += pdf_to_text(pdf)

    with open('f_t.txt' , 'w') as fil : fil.write(full_text)


extract_text_as_unstructured()
extract_text_as_headings()
extract_full_text()