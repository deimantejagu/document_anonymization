import os
import re
import spacy
from pathlib import Path
from docx import Document
from spacy import displacy

def anonymize_documents(documents_folder, processed_documents_folder, model_path):
    # Load the SpaCy model
    nlp = spacy.load(model_path)

    # Load the document
    files = os.listdir(f"{documents_folder}/")
    for file in files:
        file_path = f"{documents_folder}/{file}"
        doc = Document(file_path)
        
        html = ""

        for paragraph in doc.paragraphs:
            # Extract text from the paragraph
            processed_text = nlp(paragraph.text)
            html += displacy.render(processed_text, style="ent")

            # Change full names to initials
            for ent in processed_text.ents:
                if ent.label_ == "PERSON":
                    initials = re.sub(r'[^A-ZĄČĘĖĮŠŲŪŽ]', '', str(ent))  # Extract initials
                    if len(initials) == 2:
                        paragraph.text = paragraph.text.replace(ent.text, f"{initials[0]}. {initials[1]}.")
                    else:
                        paragraph.text = paragraph.text.replace(ent.text, f"{initials}.")

            # Delete personal code
            paragraph.text = re.sub(r',?\s*\.?(a\.k)?\.\s*\d{11},?', '', paragraph.text)

            # Delete birth date
            paragraph.text = re.sub(r'\.?,?\s*\bgim\w*\.?\s*(\d{4}-\d{2}-\d{2}|\d{4})?\s*m?.?,?', '', paragraph.text)

        # Save the modified document
        doc.save(f"{processed_documents_folder}/{file}")

        with open(f"{processed_documents_folder}/html/{Path(file).stem}.html", "w", encoding="UTF-8") as f:
            f.write(html)