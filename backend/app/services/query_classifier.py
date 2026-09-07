from enum import Enum
import re

class QueryType(str, Enum):
    STATIC_KNOWLEDGE = "STATIC_KNOWLEDGE"
    SPATIAL_QUERY = "SPATIAL_QUERY"
    HYBRID_QUERY = "HYBRID_QUERY"

class QueryClassifier:
    def __init__(self):
        self.spatial_keywords = [
            "see", "visible", "from here", "nearby", "distance", 
            "दिसू", "पाहू", "इथून", "जवळ", "अंतर"
        ]
        
        self.static_keywords = [
            "history", "built", "who", "when", "year", "story",
            "इतिहास", "कोणी", "कधी", "वर्ष", "माहिती", "बांधला"
        ]

    def classify(self, query: str) -> QueryType:
        query_lower = query.lower()
        
        has_spatial = any(keyword in query_lower for keyword in self.spatial_keywords)
        has_static = any(keyword in query_lower for keyword in self.static_keywords)
        
        if has_spatial and has_static:
            return QueryType.HYBRID_QUERY
        elif has_spatial:
            return QueryType.SPATIAL_QUERY
        else:
            # Default to static knowledge if no clear spatial intent
            return QueryType.STATIC_KNOWLEDGE

query_classifier = QueryClassifier()
