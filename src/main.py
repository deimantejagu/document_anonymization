from model_train_validate import train_spacy
from document_anonymization import anonymize_documents
from utils.dataset_generator import generate_dataset

# Generate dataset
# generate_dataset(30000, 4000)

# Train model
train_spacy("src/spaCy/model", "src/spaCy/optimizer.pkl", "src/dataset/train_dataset.json", "src/dataset/validation_dataset.json", 50, 64, 2)

# Test model
# Run document anonymization
# anonymize_documents("src/documents", "src/processed_documents", "src/spaCy/model")
