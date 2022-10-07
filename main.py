from fastapi import FastAPI
from pydantic import BaseModel

import spacy

app = FastAPI()
try:
    nlp = spacy.load("da_core_news_lg")
except: # If not present, we download
    spacy.cli.download("da_core_news_lg")
    nlp = spacy.load("da_core_news_lg")

class Item(BaseModel):
    text: str

    def anonymize(self):
      doc = nlp(self.text)
      cleaned_text = self.text
      for ent in reversed(doc.ents):
        if ent.label_ == "PER":
          cleaned_text = cleaned_text[:ent.start_char] + "[ANONYMIZED]" + cleaned_text[ent.end_char:]
      return cleaned_text

@app.get("/")
async def root():
    return {"message":"Anonymizer"}

@app.post("/anonymize")
async def anonymize(item: Item):
    return item.anonymize()
