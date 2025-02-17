from model_training_and_testing import train_spacy, test_spacy
from document_anonymization import anonymize_documents

# Train model
train_spacy("src/spaCy/best_model", "src/spaCy/best_optimizer.pkl", "src/dataset/train_dataset.json")

# Test model
test_spacy("src/spaCy/best_model", "src/dataset/test_dataset.json")

# Run document anonymization
# anonymize_documents("src/documents", "src/processed_documents", "src/spaCy/best_model")
