from fastapi import FastAPI, Query
from scholarly import scholarly
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Scholarly Google Scholar API",
    description="Een eenvoudige API om zoekresultaten van Google Scholar op te halen met Scholarly.",
    version="1.0.0"
)

# CORS-middleware zodat andere systemen (zoals GPTs) deze API kunnen aanroepen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_scholar(query: str = Query(..., description="Zoekterm voor Google Scholar")):
    """
    Doorzoek Google Scholar voor academische publicaties.
    """
    search_query = scholarly.search_pubs(query)
    results = []

    for _ in range(5):  # Haal maximaal 5 resultaten op
        try:
            pub = next(search_query)
            bib = pub.get("bib", {})
            results.append({
                "title": bib.get("title"),
                "author": bib.get("author"),
                "year": bib.get("pub_year"),
                "abstract": bib.get("abstract"),
                "url": f"https://scholar.google.com/scholar_lookup?title={bib.get('title', '').replace(' ', '+')}"
            })
        except StopIteration:
            break
        except Exception as e:
            return {"error": str(e)}

    return {"results": results}
    @app.get("/")
def root():
    return {"message": "Scholarly API is live! Gebruik /search?query=..."}
