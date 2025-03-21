from fastapi import FastAPI, Query
from scholarly import scholarly
from fastapi.middleware.cors import CORSMiddleware
import logging

# Zet logging aan
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Scholarly Google Scholar API",
    description="Een eenvoudige API om zoekresultaten van Google Scholar op te halen met Scholarly.",
    version="1.0.0"
)

# ✅ CORS-instellingen zodat GPT verbinding mag maken
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OF: ["https://chat.openai.com"] voor meer restrictie
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🎓 Scholarly API is live! Gebruik /search?query=... om artikelen op te halen."
    }

@app.get("/search")
def search_scholar(query: str = Query(..., description="Zoekterm voor Google Scholar")):
    """
    Doorzoek Google Scholar voor academische publicaties via Scholarly.
    """
    try:
        search_query = scholarly.search_pubs(query)
        results = []

        for i in range(5):  # Haal max 5 artikelen op
            try:
                pub = next(search_query)
                bib = pub.get("bib", {})
                result = {
                    "title": bib.get("title"),
                    "author": bib.get("author"),
                    "year": bib.get("pub_year"),
                    "abstract": bib.get("abstract"),
                    "url": f"https://scholar.google.com/scholar_lookup?title={bib.get('title', '').replace(' ', '+')}"
                }
                results.append(result)
                logging.info(f"[{i+1}] Artikel gevonden: {result['title']}")
            except StopIteration:
                break
            except Exception as e:
                logging.warning(f"Probleem bij ophalen publicatie: {str(e)}")
                continue

        return {"results": results}

    except Exception as e:
        logging.error(f"Fout in hoofdzoekopdracht: {str(e)}")
        return {"error": "Er is iets misgegaan tijdens het zoeken."}
