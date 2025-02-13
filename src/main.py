from utils import create_names_patterns
from model_training_and_testing import train_spacy, test_spacy
from document_anonymization import anonymize_documents

# Uncomment if you need to generate new names with whom you will create new texts for model training dataset
# names = create_names_patterns()
# save_data("/NER/src/dataset/names.json", names)

# Train model
# train_spacy("src/spaCy/best_model", "src/spaCy/best_optimizer.pkl", "src/dataset/train_dataset.json", 5)

# Test model
test_spacy("src/spaCy/best_model", "src/dataset/test_dataset.json")

# Run document anonymization
# anonymize_documents("src/documents", "src/processed_documents", "src/spaCy/best_model")