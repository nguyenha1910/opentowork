import fitz  # PyMuPDF library
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_lg") # python -m spacy download en_core_web_lg

def skill_extraction(path):
    with fitz.open(path) as pdf_resume:
        extracted_resume_content_PyMuPDF = ""
        for page_number in range(pdf_resume.page_count):
            page = pdf_resume[page_number]
            extracted_resume_content_PyMuPDF += page.get_text()

    # print statement that checks the content
    #print("extracted_resume_content_PyPDF4:", extracted_resume_content_PyMuPDF)

    # needs to have this file downloaded
    skills = "jz_skill_patterns.jsonl" 
    # https://medium.com/@vikrantptl06/resume-parsing-using-spacy-af24376ec008
    # https://github.com/kingabzpro/jobzilla_ai/blob/main/jz_skill_patterns.jsonl

    ruler = nlp.add_pipe("entity_ruler", before = "ner")
    ruler.from_disk(skills)
    doc = nlp(extracted_resume_content_PyMuPDF)

    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]

    dict = {}
    skills = []

    for ent in doc.ents:
        #print(ent.label_)
        if "SKILL" in ent.label_:
            skills.append(ent.text)

    # remove duplicates (capitalization)
    lowercase_skills = [s.lower() for s in skills]
    unique_skills = list(set(lowercase_skills))
    return unique_skills

