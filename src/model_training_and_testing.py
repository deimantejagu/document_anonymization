import spacy
import random
import pickle
from utils import load_data, save_data
from spacy.training import Example
from sklearn.metrics import precision_score, recall_score, f1_score

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
                nlp.to_disk(f"src/spaCy/best_model")
                with open(f"src/spaCy/best_optimizer.pkl", "wb") as f:
                    pickle.dump(optimizer, f)
                print(f"Checkpoint saved at {itn} iteration")

def test_spacy(model_path, data):
    nlp = spacy.load(model_path)
    lines = load_data(data)
    true_entities_all = []
    pred_entities_all = []
    predictions = []
    for line, annotation in lines:
        labels = [tuple(x) for x in annotation["entities"]]
        doc = nlp(line)
        pred_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

        label_set = set(labels)
        prediction_set = set(pred_entities)

        for label in label_set:
            true_entities_all.append(1)
            if label in prediction_set:
                pred_entities_all.append(1)
            else:
                pred_entities_all.append(0)

        for prediction in prediction_set:
            if prediction not in label_set:
                true_entities_all.append(0)
                pred_entities_all.append(1)

        entities_texts = [ent.text for ent in doc.ents]
        predictions.append([line, {"entities": entities_texts}])

    precision = precision_score(true_entities_all, pred_entities_all) * 100
    recall = recall_score(true_entities_all, pred_entities_all) * 100
    f1 = f1_score(true_entities_all, pred_entities_all) * 100

    print(f"Precision: {precision:.3f} %")
    print(f"Recall: {recall:.3f} %")
    print(f"F1-score: {f1:.3f} %")

    save_data("/NER/src/dataset/predictions.json", predictions)
