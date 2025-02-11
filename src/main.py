import re
import os
import spacy
from pathlib import Path
from spacy import displacy
from docx import Document
from faker import Faker
from spacy.pipeline import EntityRuler
from spacy.training import Example
from spacy.lang.lt import Lithuanian
import json
import random

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
    for i in range(400):
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

    with open("/NER/src/model/entity_ruler/patterns.jsonl", "w", encoding="utf-8") as f:
        for pattern in patterns:
            json.dump(pattern, f, ensure_ascii=False)  
            f.write("\n")

# patterns = create_training_data("PERSON")
# generate_rules(patterns)
# print(len(patterns))

def test_model(model, text):
    doc = model(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        return(results)

# TRAIN_DATA = [(text, {entities: [(start, end, label)]})]

# nlp = spacy.load("src/model")

# TRAIN_DATA = []
# with open("src/text.txt", "r", encoding="UTF-8") as f:
#     text = f.read()
#     lines = text.split("\n")
#     for line in lines:
#         results = test_model(nlp, line)
#         if results != None:
#             TRAIN_DATA.append(results)

def save_data(file, data):
    with open(file, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)   

# save_data("/NER/src/train_dataset.json", TRAIN_DATA)

def load_data(file):
    with open(file, "r", encoding="UTF-8") as f:
        data = json.load(f)

    return data

def train_spacy(data, iterations):
    nlp = spacy.blank("lt")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)

    for _, annotations in data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
            
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(data)
            losses = {}
            examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in data]
            for example in examples:
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
            print(f"NER Loss: {losses['ner']:.4f}")

        # Save the model checkpoint
        if itn % 10 == 0:
            model_path = f"src/model_checkpoint_{itn}"
            nlp.to_disk(model_path)
            print(f"Checkpoint saved to {model_path}")

    return nlp

TRAIN_DATA = load_data("/NER/src/train_dataset.json")
nlp = train_spacy(TRAIN_DATA, 30)
nlp.to_disk("src/model")
