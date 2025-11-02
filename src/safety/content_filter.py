"""
Content Safety Filter
Responsible AI - Detect harmful queries and inappropriate content
"""

import re

class ContentFilter:
    """Basic content filtering for educational AI tutor."""

    # Keywords that indicate harmful or inappropriate content
    BLOCKED_KEYWORDS = [
        # Violence/Harm
        "Kill", "murder", "suicide", "hurt yourself",
        # Inappropriate
        "hack", "cheat", "exam answers", "homework answers", "nsfw",
        # Personal info requests
        "phone number", "address", "password", "social security", "credit card", "adhaar card"
        
    ]

    # Education boundary keywords
    OUT_OF_SCOPE = [
        "love advice", "relationship", "dating",
        "politics", "religion", "financial advice"
    ]

    @staticmethod
    def is_safe(query):
        """Check if the query is safe for processing."""

        query_lower = query.lower()
        # Check for blocked keywords
        for keyword in ContentFilter.BLOCKED_KEYWORDS:
            if keyword in query_lower:
                return False, "Your query contains inappropriate or harmful content and cannot be processed."

        # Check for out-of-scope topics
        for topic in ContentFilter.OUT_OF_SCOPE:
            if keyword in query_lower:
                return False, "Your query is outside the educational scope of this AI tutor."

        return True, ""
    
    @staticmethod
    def add_safety_context(response):
        """"Add disclaimer to the AI response."""

        # If response contains problem solving
        if any(word in response.lower() for word in ["solve", "solution", "answer", "calculate"]):
            response += "\n\n*Disclaimer: The solution provided is for educational purposes only. Please ensure you understand the steps involved.*"
        
        return response
