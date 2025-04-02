import spacy

nlp = spacy.load("en_core_web_sm")

cooking_terms = {
    "al dente": "Al dente describes pasta that is cooked until it is firm when bitten, not too soft.",
    "sauté": "Sautéing means cooking food quickly in a small amount of oil over medium-high heat.",
    "blanch": "Blanching is boiling food for a short time and then cooling it rapidly to stop cooking."
}

allergens = {"milk", "cheese", "butter", "flour", "bread", "nuts", "peanuts", "almonds", "cashews", "eggs", "soy", "shellfish"}

def extract_intent_and_entities(user_input):
    """Analyze user message using NLP to extract intent and entities."""
    doc = nlp(user_input.lower())

    # Intent detection based on keywords
    if any(token.lemma_ in ["allergen", "allergy", "contain"] for token in doc):
        intent = "allergen_check"
    elif any(token.lemma_ in ["replace", "substitute"] for token in doc):
        intent = "substitution"
    elif any(token.lemma_ in ["cook", "boil", "bake", "al dente"] for token in doc):
        intent = "cooking_explanation"
    else:
        intent = "recipe_request"

    # Extract ingredients or cooking terms
    entities = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    return intent, entities

def explain_cooking_term(term):
    """Fetch explanation for a cooking term"""
    return cooking_terms.get(term.lower(), "I’m not sure, but I can look it up for you!")
