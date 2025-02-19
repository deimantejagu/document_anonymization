import random
from collections import defaultdict, Counter
from .file_storage import save_data
from .names_generator import create_names_patterns
from .dataset_phrases import INTRODUCTIONS, ACTIONS, CONCLUSIONS

def balance_phrases(phrase_list):
    counter = Counter(phrase_list)
    
    def get_balanced_phrase():
        # Select the phrase with the minimum usage count
        phrase = min(phrase_list, key=lambda x: counter[x])
        counter[phrase] += 1
        return phrase

    return get_balanced_phrase

def check_overlap(existing_entities, new_entity):
    new_start, new_end, _ = new_entity
    for start, end, _ in existing_entities:
        # Overlap occurs if the new span intersects any existing span
        if not (new_end <= start or new_start >= end):
            return True
    return False

def remove_substring_names(chosen_names):
    filtered = []
    for n in chosen_names:
        # If `n` is a substring of something in `filtered` OR
        # something in `filtered` is a substring of `n`, skip it.
        if any(n in f or f in n for f in filtered if n != f):
            continue
        filtered.append(n)
    return filtered

def generate_dataset(num_sentences, names_counter):
    all_names = create_names_patterns(names_counter)
    random.shuffle(all_names)

    name_counts = defaultdict(int)  # track usage of each name

    get_intro = balance_phrases(INTRODUCTIONS)
    get_action = balance_phrases(ACTIONS)
    get_conclusion = balance_phrases(CONCLUSIONS)

    one_third = num_sentences // 3
    sentence_lengths = (
        ["short"] * one_third +
        ["medium"] * one_third +
        ["long"] * (num_sentences - 2 * one_third)
    )
    random.shuffle(sentence_lengths)

    dataset = []
    for i in range(num_sentences):
        intro = get_intro()
        action = get_action()
        conclusion = get_conclusion()

        chosen_full_names = random.sample(all_names, random.randint(1, 2))
        chosen_full_names = remove_substring_names(chosen_full_names)

        # Update usage counts
        for name in chosen_full_names:
            name_counts[name] += 1

        # Pick a sentence structure
        sentence_type = sentence_lengths[i]

        if sentence_type == "short":
            final_sentence = f"{i+1}. {intro}, {random.choice(ACTIONS)}, kartu su {chosen_full_names[0]}."
        elif sentence_type == "medium":
            if chosen_full_names:
                final_sentence = f"{i+1}. {intro}, {action}, kartu su {chosen_full_names[0]}, {conclusion}."
            else:
                final_sentence = f"{i+1}. {intro}, {action}, {conclusion}."
        else:
            if chosen_full_names:
                final_sentence = f"{i+1}. {intro}, {action}, kartu su {', '.join(chosen_full_names)}, {conclusion}."
            else:
                final_sentence = f"{i+1}. {intro}, {action}, {conclusion}."

        # Now find occurrences of each name without overlapping entities
        entities = []
        for name in chosen_full_names:
            start_search = 0
            while True:
                # Find the next occurrence of `name` in `final_sentence`
                start_idx = final_sentence.find(name, start_search)
                if start_idx == -1:
                    break
                end_idx = start_idx + len(name)
                new_entity = (start_idx, end_idx, "PERSON")

                # Add only if it doesn't overlap existing entities
                if not check_overlap(entities, new_entity):
                    entities.append(new_entity)

                # Move the search index forward to avoid infinite loop
                start_search = end_idx

        entities.sort(key=lambda ent: ent[0])

        dataset.append([final_sentence, {"entities": entities}])

    save_data("src/dataset/train_dataset.json", dataset)