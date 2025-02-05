# docker build -t ner .
# docker run -v C:/Users/Testinis/Desktop/spacy_named_entitty_recognition/src:/NER/src ner
# docker run -v /Users/deimantejagucanskyte/Documents/work/spacy_named_entity_recognition/src:/NER/src ner
FROM python:3.11

# Force BLIS to fallback to a generic config instead of cortexa57
ENV BLIS_ARCH=generic

# Set the working directory in the container
WORKDIR /NER

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential gcc

# Upgrade pip and related tools
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy model
RUN python -m spacy download lt_core_news_lg

# Copy the rest of the application code into the container
COPY ./src /NER/src

# Command to run the application
CMD ["python", "src/main.py"]
