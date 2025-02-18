import random
from .file_storage import save_data
from .names_generator import create_names_patterns
from .dataset_phrases import INTRODUCTIONS, ACTIONS, CONCLUSIONS

def generate_dataset(num_sentences, names_counter):
    all_names = create_names_patterns(names_counter)
    random.shuffle(all_names)

    random.shuffle(INTRODUCTIONS)
    random.shuffle(ACTIONS)
    random.shuffle(CONCLUSIONS)

    dataset = []
    for i in range(1, num_sentences + 1):
        intro = random.choice(INTRODUCTIONS)
        action = random.choice(ACTIONS)
        conclusion = random.choice(CONCLUSIONS)
        
        chosen_full_names = random.sample(all_names, random.randint(1, 5))
        
        sentence_start = f"{i}. {intro}, "
        final_sentence = sentence_start
        entities = []

        pos_cursor = len(final_sentence)
        
        for idx, mention in enumerate(chosen_full_names):
            start_idx = pos_cursor
            final_sentence += mention
            end_idx = start_idx + len(mention)
            
            entities.append([start_idx, end_idx, "PERSON"])
            
            pos_cursor = len(final_sentence)
            
            if idx < len(chosen_full_names) - 1:
                if idx == len(chosen_full_names) - 2:
                    final_sentence += " ir "
                    pos_cursor += 4
                else:
                    final_sentence += ", "
                    pos_cursor += 2
        
        final_sentence += f" {action}, {conclusion}."
        dataset.append([final_sentence, {"entities": entities}])

    save_data("src/dataset/train_dataset.json", dataset)
