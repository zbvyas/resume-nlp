"""
This script extract key information from a resume using Apache Tika and NLTK
"""
import re
import argparse
from pprint import pprint
import nltk
import tika
from tika import parser

p = argparse.ArgumentParser()
p.add_argument(
    '-f', '--file', help='Filepath to the docx/pdf resume', required=True)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

tika.initVM()

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

# you may read the database from a csv file or some other database
DEVELOPER_SKILLS = [
    'python',
    'java',
    'javascript',
    'typescript',
    'git',
    'mysql',
    'postgresql'
]


def extract_text_from_docx(docx_path):
    """
    Extract all unstructured text from the resume
    """
    cleaned = None
    parsed = parsed = parser.from_file(docx_path)
    cleaned = parsed['content'].replace('\n', '')
    cleaned = cleaned.replace('\t', ' ')
    return cleaned


def extract_names(resume_text):
    """
    Extract names from the resume
    """
    person_names = []

    for sent in nltk.sent_tokenize(resume_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )

    return person_names


def extract_phone_number(resume_text):
    """
    Extract phone number from the resume
    """
    phone = re.findall(PHONE_REG, resume_text)

    if phone:
        number = ''.join(phone[0])
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None


def extract_emails(resume_text):
    """
    Extract email addresses from the resume
    """
    return re.findall(EMAIL_REG, resume_text)


def extract_skills(resume_text):
    """
    Extract skills from the resume
    """
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(resume_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in DEVELOPER_SKILLS:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in DEVELOPER_SKILLS:
            found_skills.add(ngram)

    return found_skills


if __name__ == '__main__':
    args = p.parse_args()
    resume_text = extract_text_from_docx(args.file)

    names = extract_names(resume_text)
    phone_number = extract_phone_number(resume_text)
    emails = extract_emails(resume_text)
    skills = extract_skills(resume_text)

    print("*"*50)
    print("NAME")
    pprint(names)

    print("*"*50)
    print("PHONE NUMBER")
    pprint(phone_number)

    print("*"*50)
    print("EMAILS")
    pprint(emails)

    print("*"*50)
    print("SKILLS")
    pprint(skills)
