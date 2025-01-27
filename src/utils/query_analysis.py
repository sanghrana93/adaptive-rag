def determine_query_complexity(query):
    """
    Determine the complexity of a query based on its length and keywords.
    """
    simple_keywords = ["what", "who", "when", "where", "how"]
    if len(query.split()) <= 5 and any(keyword in query.lower() for keyword in simple_keywords):
        return "simple"
    else:
        return "complex"