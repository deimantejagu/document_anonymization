import spacy
from spacy.training import Example
import random
import pickle
from utils import save_data, load_data

def train_spacy(model_path, optimizer_path, data_path, iterations):
    nlp = spacy.load(model_path)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    data = load_data(data_path)
    for _, annotations in data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    best_loss = float("inf")

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        if optimizer_path is not None:
            with open(optimizer_path, "rb") as f:
                optimizer = pickle.load(f)
        else:
            optimizer = nlp.begin_training()
            
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(data)
            losses = {}
            examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in data]
            for example in examples:
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
            ner_loss = losses.get("ner", 0)
            print(f"NER Loss: {ner_loss:.4f}")

            # Save the model checkpoint and optimizer
            if ner_loss < best_loss:
                best_loss = ner_loss
                nlp.to_disk(f"src/spaCy/optimizer_checkpoint_{itn}.pkl")
                with open(f"src/spaCy/model_checkpoint_{itn}", "wb") as f:
                    pickle.dump(optimizer, f)
                print(f"Checkpoint saved at iteration {itn}")

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
    lines = load_data(data)
    predictions = []  
    for line in lines:
        doc = nlp(line[0])
        entities = [ent.text for ent in doc.ents]
        if entities: 
            prediction = [line[0], {"entities": entities}]
            predictions.append(prediction)

    save_data("/NER/src/predictions.json", predictions)
