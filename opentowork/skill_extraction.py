import fitz  # PyMuPDF library
import spacy
import pandas as pd
import os

nlp = spacy.load("en_core_web_lg") # python -m spacy download en_core_web_lg

def skill_extraction(path):
    if os.path.splitext(path)[1].lower() != ".pdf":
        raise ValueError("Invalid file format. Only PDF files are supported.")

    with fitz.open(path) as pdf_resume:
        extracted_resume_content_PyMuPDF = ""
        for page_number in range(pdf_resume.page_count):
            page = pdf_resume[page_number]
            extracted_resume_content_PyMuPDF += page.get_text()

    # needs to have this file downloaded
    skills = "raw/jz_skill_patterns.jsonl" 
    # https://github.com/kingabzpro/jobzilla_ai/blob/main/jz_skill_patterns.jsonl

    if "entity_ruler" not in nlp.pipe_names:
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

if __name__ == "__main__":
    path = "pdfs/random_ds_resume.pdf"
    skills = skill_extraction(path)
    print(skills)