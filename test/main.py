import re
import random
from faker import Faker

fake = Faker('lt_LT')

MALE_NAME_ENDINGS = ['as', 'is', 'us']
FEMALE_NAME_ENDINGS = ['a', 'ė', 'i', 'utė', 'ytė', 'elė']

MALE_LAST_NAME_ENDINGS = ['as', 'is', 'us', 'a', 'ius', 'jus', 'ys']
FEMALE_LAST_NAME_ENDINGS = ['aitė', 'ytė', 'utė', 'iūtė', 'ūtė', 'ė', 'ienė', 'uvienė', 'iuvienė']

NAMES = []

i = 0
while i < 10:
    first_name = fake.first_name() 
    last_name = fake.last_name()  

    # last_name = re.sub(r'(' + '|'.join(MALE_LAST_NAME_ENDINGS) + r')$', random.choice(MALE_LAST_NAME_ENDINGS), last_name)

    if first_name.endswith(tuple(FEMALE_NAME_ENDINGS)):
        print(f"{first_name}")
    elif first_name.endswith(tuple(MALE_NAME_ENDINGS)):
        print(f"{first_name}")

    # NAMES.append((f'{first_name} {last_name}'))
    i += 1

# # Print generated names
# for name in NAMES:
#     print(name)
