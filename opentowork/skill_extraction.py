"""
module of PyMuPdf library for pdf format resume parsing
spacy module for entity assignment and extraction of skill set from a user's resume
"""
import os
import yaml
import spacy
import fitz  # PyMuPDF library


with open("config.yml", "r", encoding='UTF-8') as config_file:
    config = yaml.safe_load(config_file)

nlp = spacy.load("en_core_web_lg") # python -m spacy download en_core_web_lg

def skill_extraction_resume(path):
    """
    parse the resume in a pdf format and extract a unique list of skill set
    that will be compared to job description
    Args:
        path (string): source path for uploaded resume file

    Returns:
        list of string : returns the list of string consists of unique skils
    """

    if os.path.splitext(path)[1].lower() != ".pdf":
        raise ValueError("Invalid file format. Only PDF files are supported.")

    with fitz.open(path) as pdf_resume:
        resume = ""
        for page_number in range(pdf_resume.page_count):
            page = pdf_resume[page_number]
            resume += page.get_text()

    skill_patterns_path = config['pattern_path']
    if not os.path.isfile(skill_patterns_path):
        link = "https://github.com/kingabzpro/jobzilla_ai/blob/main/jz_skill_patterns.jsonl"
        raise FileNotFoundError(
            f"{skill_patterns_path} not found.\
            \nPlease download the file from {link}")

    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before = "ner")
        ruler.from_disk(skill_patterns_path)
    doc = nlp(resume)
    skill_patterns_path = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]

    for ent in doc.ents:
        if "SKILL" in ent.label_:
            skill_patterns_path.append(ent.text)

    # remove duplicates (capitalization)
    lowercase_skills = [s.lower() for s in skill_patterns_path]
    unique_skills = list(set(lowercase_skills))
    return unique_skills

def skill_extraction_job_description(description_row):
    """
    Extract the skill set from the job description  
    Args:
        description_row (string): job description
    Returns:
        list of string : returns the list of string consists of unique skils
    """

    skill_patterns_path = config['pattern_path']
    if not os.path.isfile(skill_patterns_path):
        link = "https://github.com/kingabzpro/jobzilla_ai/blob/main/jz_skill_patterns.jsonl"
        raise FileNotFoundError(
            f"{skill_patterns_path} not found.\
            \nPlease download the file from {link}")

    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before = "ner")
        ruler.from_disk(skill_patterns_path)

    doc = nlp(description_row)
    skill_patterns_path = [ent.text for ent in doc.ents if "SKILL" in ent.label_]

    # remove duplicates (capitalization)
    lowercase_skills = [s.lower() for s in skill_patterns_path]
    unique_skills = list(set(lowercase_skills))
    return unique_skills
