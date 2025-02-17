from model_train_validate import train_spacy
from document_anonymization import anonymize_documents

# Train model
train_spacy("src/spaCy/model", "src/spaCy/optimizer.pkl", "src/dataset/train_dataset.json", "src/dataset/validation_dataset.json", 30, 16, 2)

# Test model
# Run document anonymization
# anonymize_documents("src/documents", "src/processed_documents", "src/spaCy/model")
