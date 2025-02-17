from model_training_and_testing import train_spacy
from document_anonymization import anonymize_documents

# Train model
train_spacy("src/spaCy/best_model", "src/spaCy/best_optimizer.pkl", "src/dataset/train_dataset.json", "src/dataset/validation_dataset.json", 100, 16, 5)

# Test model
# Run document anonymization
# anonymize_documents("src/documents", "src/processed_documents", "src/spaCy/best_model")
