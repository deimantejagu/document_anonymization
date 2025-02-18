import re
from faker import Faker

MALE_NAME_ENDINGS = ['as', 'is', 'us']
FEMALE_NAME_ENDINGS = ['a', 'ė', 'i', 'utė', 'ytė', 'elė']

MALE_LAST_NAME_ENDINGS = ['as', 'is', 'us', 'a', 'ius', 'jus', 'ys']
FEMALE_LAST_NAME_ENDINGS = ['aitė', 'ytė', 'utė', 'iūtė', 'ūtė', 'ė', 'ienė', 'uvienė', 'iuvienė']

fake = Faker('lt_LT')

def generate_names(endings_array, first_name):
    temp_names = []
    last_name = fake.last_name()  
    last_name_base = re.sub(r'(' + '|'.join(MALE_LAST_NAME_ENDINGS) + r')$', '', last_name)
    initials = re.search(r'[A-ZĄČĘĖĮŠŲŪŽ]', str(first_name))
    for ending in endings_array:
        generated_last_name = f'{last_name_base}{ending}'
        temp_names.append((f'{first_name} {generated_last_name}'), )
        temp_names.append(f'{initials.group()}. {generated_last_name}')
        temp_names.append(generated_last_name)

    return temp_names

def select_names_generator(first_name):
    if first_name.endswith(tuple(FEMALE_NAME_ENDINGS)):
        return generate_names(FEMALE_LAST_NAME_ENDINGS, first_name)
    elif first_name.endswith(tuple(MALE_LAST_NAME_ENDINGS)):
        return generate_names(MALE_LAST_NAME_ENDINGS, first_name)
    
def create_names_patterns(names_counter):
    names = []

    for i in range(names_counter):
        sub_list = select_names_generator(fake.first_name())
        names.extend(sub_list)

    return names
