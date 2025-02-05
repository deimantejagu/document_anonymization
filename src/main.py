import spacy
import re
import os
from pathlib import Path
from spacy import displacy
from docx import Document

# Load the SpaCy model
nlp = spacy.load("lt_core_news_lg")

# Load the document
base_path = 'src/files/'
files = os.listdir(base_path)
for file in files:
    file_path = f"{base_path}{file}"
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
    doc.save(f"src/processed_files/{file}")

    with open(f"src/processed_files/{Path(file).stem}.html", "w", encoding="UTF-8") as f:
        f.write(html)