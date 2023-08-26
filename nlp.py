import spacy

nlp = spacy.load("en_core_web_sm")

def get_entities(sentence):
    doc = nlp(sentence)
    return [(ent.text, ent.label_) for ent in doc.ents]
