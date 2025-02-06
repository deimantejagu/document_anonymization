import re
import os
import spacy
from pathlib import Path
from spacy import displacy
from docx import Document
from faker import Faker
from spacy.pipeline import EntityRuler
from spacy.lang.lt import Lithuanian
import json

# # Load the SpaCy model
# nlp = spacy.load("lt_core_news_lg")

# # Load the document
# base_path = 'src/files/'
# files = os.listdir(base_path)
# for file in files:
#     file_path = f"{base_path}{file}"
#     doc = Document(file_path)
    
#     html = ""

#     for paragraph in doc.paragraphs:
#         # Extract text from the paragraph
#         processed_text = nlp(paragraph.text)
#         html += displacy.render(processed_text, style="ent")

#         # Change full names to initials
#         for ent in processed_text.ents:
#             if ent.label_ == "PERSON":
#                 initials = re.sub(r'[^A-ZĄČĘĖĮŠŲŪŽ]', '', str(ent))  # Extract initials
#                 if len(initials) == 2:
#                     paragraph.text = paragraph.text.replace(ent.text, f"{initials[0]}. {initials[1]}.")
#                 else:
#                     paragraph.text = paragraph.text.replace(ent.text, f"{initials}.")

#         # Delete personal code
#         paragraph.text = re.sub(r',?\s*\.?(a\.k)?\.\s*\d{11},?', '', paragraph.text)

#         # Delete birth date
#         paragraph.text = re.sub(r'\.?,?\s*\bgim\w*\.?\s*(\d{4}-\d{2}-\d{2}|\d{4})?\s*m?.?,?', '', paragraph.text)

#     # Save the modified document
#     doc.save(f"src/processed_files/{file}")

#     with open(f"src/processed_files/{Path(file).stem}.html", "w", encoding="UTF-8") as f:
#         f.write(html)

fake = Faker('lt_LT')

MALE_NAME_ENDINGS = ['as', 'is', 'us']
FEMALE_NAME_ENDINGS = ['a', 'ė', 'i', 'utė', 'ytė', 'elė']

MALE_LAST_NAME_ENDINGS = ['as', 'is', 'us', 'a', 'ius', 'jus', 'ys']
FEMALE_LAST_NAME_ENDINGS = ['aitė', 'ytė', 'utė', 'iūtė', 'ūtė', 'ė', 'ienė', 'uvienė', 'iuvienė']

NAMES = []

def generate_names(endings_array, first_name):
    last_name = fake.last_name()  
    last_name_base = re.sub(r'(' + '|'.join(MALE_LAST_NAME_ENDINGS) + r')$', '', last_name)
    initials = re.search(r'[A-ZĄČĘĖĮŠŲŪŽ]', str(first_name))
    for ending in endings_array:
        generated_last_name = f'{last_name_base}{ending}'
        NAMES.append((f'{first_name} {generated_last_name}'), )
        NAMES.append(f'{initials.group()}. {generated_last_name}')
        NAMES.append(generated_last_name)

def select_names_generator(first_name):
    if first_name.endswith(tuple(FEMALE_NAME_ENDINGS)):
        generate_names(FEMALE_LAST_NAME_ENDINGS, first_name)
    elif first_name.endswith(tuple(MALE_LAST_NAME_ENDINGS)):
        generate_names(MALE_LAST_NAME_ENDINGS, first_name)

def create_training_data(type):
    for i in range(10000):
        select_names_generator(fake.first_name())

    patterns = []
    for item in NAMES:
        pattern = { 
            "label": type,
            "pattern": item
        }
        patterns.append(pattern)

    return patterns

def generate_rules(patterns):
    nlp = Lithuanian()
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    nlp.to_disk("/NER/src/model") 

patterns = create_training_data("PERSON")
generate_rules(patterns)
# print(patterns)
# print(len(patterns))

# # Print generated names
# for name in NAMES:
#     print(name)
# print(len(NAMES))

def test_model(model, text):
    doc = model(text)
    results = []
    for ent in doc.ents:
        results.append(ent.text)

    return(results)

def save_data(file, data):
    with open(file, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)

nlp = spacy.load("src/model")

with open("src/text.txt", "r") as f:
    text = f.read()
    hits = []
    results = test_model(nlp, text)
    for result in results:
        hits.append(result)
print(hits)      

save_data("/NER/src/results.json", hits)