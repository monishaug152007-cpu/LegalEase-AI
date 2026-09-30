import os, requests
from dotenv import load_dotenv
load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    def generate_document(self, document_type, parties, terms, dates):
        if not self.api_key or self.api_key == "paste_your_api_key_here":
            raise RuntimeError("Gemini API key missing. Add it to .env in the project folder.")
        clauses = [x.strip() for x in terms.split(";") if x.strip()]
        prompt = f"""Draft a structured first-pass {document_type} using only the supplied details.
Parties: {parties}
Effective date: {dates}
Terms and conditions:
{chr(10).join("- " + x for x in clauses)}
Use a formal title, numbered headings, and readable paragraphs. Do not invent facts, addresses, amounts, or legal citations. Mark missing essential details [DETAIL REQUIRED]. End with: Draft for review only. This is not legal advice. Consult a qualified lawyer before signing. Return plain text only."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        try:
            response = requests.post(url, params={"key":self.api_key}, json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.25,"maxOutputTokens":4096}}, timeout=90)
        except requests.RequestException as exc:
            raise RuntimeError(f"Could not reach Gemini API: {exc}")
        if not response.ok:
            try: detail=response.json().get("error",{}).get("message",response.text)
            except ValueError: detail=response.text
            raise RuntimeError(f"Gemini API error {response.status_code}: {detail}")
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError, TypeError):
            raise RuntimeError("Gemini returned no document. Please try again.")
