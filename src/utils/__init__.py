from .file_storage import save_data, load_data
from .names_generator import create_names_patterns
from .dataset_generator import generate_dataset
from .dataset_phrases import INTRODUCTIONS, ACTIONS, CONCLUSIONS

__all__ = [
    "save_data",
    "load_data",
    "create_names_patterns",
    "generate_dataset"
    "INTRODUCTIONS",
    "ACTIONS",
    "CONCLUSIONS"
]