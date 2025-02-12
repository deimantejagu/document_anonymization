import spacy
from spacy.training import Example
import random
from sklearn.metrics import classification_report
from utils import save_data

def train_spacy(model_path, iterations, data):
    nlp = spacy.load(model_path)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)

    for _, annotations in data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        best_loss = 1000000000000000
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(data)
            losses = {}
            examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in data]
            for example in examples:
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
            print(f"NER Loss: {losses['ner']:.4f}")

            # Save the model checkpoint
            if losses['ner'] < best_loss:
                best_loss = losses['ner']
                model_path = f"src/model_checkpoint_{itn}"
                nlp.to_disk(model_path)
                print(f"Checkpoint saved to {model_path}")

def get_models_predictions(model, line):
    doc = model(line)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.text))
    if len(entities) > 0:
        results = [line, {"entities": entities}]

        return results

def test_spacy(model_path, data):
    nlp = spacy.load(model_path)

    train_data = []
    with open(data, "r", encoding="UTF-8") as f:
        text = f.read()
        lines = text.split("\n")
        for line in lines:
            results = get_models_predictions(nlp, line)
            if results != None:
                train_data.append(results)

    save_data("/NER/src/results.json", train_data)
