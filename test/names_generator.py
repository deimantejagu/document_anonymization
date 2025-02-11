import re
from faker import Faker

fake = Faker('lt_LT')

MALE_NAME_ENDINGS = ['as', 'is', 'us']
FEMALE_NAME_ENDINGS = ['a', 'ė', 'i', 'utė', 'ytė', 'elė']

MALE_LAST_NAME_ENDINGS = ['as', 'is', 'us', 'a', 'ius', 'jus', 'ys']
FEMALE_LAST_NAME_ENDINGS = ['aitė', 'ytė', 'utė', 'iūtė', 'ūtė', 'ė', 'ienė', 'uvienė', 'iuvienė']

NAMES = []

def generate_names(endings_array, first_name):
    last_name = fake.last_name()  
    last_name_base = re.sub(r'(' + '|'.join(MALE_LAST_NAME_ENDINGS) + r')$', '', last_name)
    initials = re.search(r'[A-ZĄČĘĖĮŠŲŪŽ]', str(first_name))
    for ending in endings_array:
        generated_last_name = f'{last_name_base}{ending}'
        NAMES.append((f'{first_name} {generated_last_name}'), )
        NAMES.append(f'{initials.group()}. {generated_last_name}')
        NAMES.append(generated_last_name)

def select_names_generator(first_name):
    if first_name.endswith(tuple(FEMALE_NAME_ENDINGS)):
        generate_names(FEMALE_LAST_NAME_ENDINGS, first_name)
    elif first_name.endswith(tuple(MALE_LAST_NAME_ENDINGS)):
        generate_names(MALE_LAST_NAME_ENDINGS, first_name)

for i in range(10000):
    select_names_generator(fake.first_name())

# Print generated names
for name in NAMES:
    print(name)

print(len(NAMES))