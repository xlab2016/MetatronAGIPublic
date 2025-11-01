"""
Concept Extractor - Heuristic-based NLP module
Extracts concepts, entities, and relationships from text without using LLMs
Uses TF-IDF, frequency analysis, and NLP techniques
"""

import re
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ConceptExtractor:
    """
    Extracts concepts from text using heuristic algorithms.
    No LLM integration - purely algorithmic approach.
    """

    def __init__(self, language='russian'):
        """
        Initialize the concept extractor.

        Args:
            language: Language for text processing ('russian' or 'english')
        """
        self.language = language
        self.stopwords = self._load_stopwords()
        self.concept_cache = {}

    def _load_stopwords(self) -> Set[str]:
        """Load stopwords for the specified language."""
        # Basic Russian stopwords
        russian_stopwords = {
            'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как',
            'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к',
            'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было',
            'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь',
            'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни',
            'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам',
            'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они',
            'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их',
            'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже',
            'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому',
            'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти',
            'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем',
            'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой',
            'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про',
            'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем',
            'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том'
        }

        # Basic English stopwords
        english_stopwords = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can',
            'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where', 'why',
            'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'of', 'in', 'to', 'for', 'with', 'from', 'by'
        }

        if self.language == 'russian':
            return russian_stopwords
        else:
            return english_stopwords

    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text: lowercase, tokenize, remove stopwords.

        Args:
            text: Input text

        Returns:
            List of preprocessed tokens
        """
        # Lowercase
        text = text.lower()

        # Extract words (Cyrillic + Latin)
        words = re.findall(r'[а-яёa-z]+', text)

        # Remove stopwords and short words
        words = [w for w in words if w not in self.stopwords and len(w) > 2]

        return words

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords using frequency analysis.

        Args:
            text: Input text
            top_n: Number of top keywords to extract

        Returns:
            List of (keyword, score) tuples
        """
        words = self.preprocess_text(text)

        # Count word frequencies
        word_freq = Counter(words)

        # Normalize scores
        if word_freq:
            max_freq = max(word_freq.values())
            keywords = [(word, freq / max_freq) for word, freq in word_freq.most_common(top_n)]
            return keywords

        return []

    def extract_concepts_tfidf(self, texts: List[str], top_n: int = 5) -> Dict[int, List[Tuple[str, float]]]:
        """
        Extract concepts using TF-IDF algorithm.

        Args:
            texts: List of text documents
            top_n: Number of top concepts per document

        Returns:
            Dictionary mapping document index to list of (concept, score) tuples
        """
        if not texts:
            return {}

        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words=list(self.stopwords),
            token_pattern=r'[а-яёa-z]+',
            lowercase=True
        )

        try:
            # Fit and transform texts
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()

            # Extract top concepts for each document
            concepts_by_doc = {}
            for doc_idx in range(len(texts)):
                doc_vector = tfidf_matrix[doc_idx].toarray()[0]
                top_indices = doc_vector.argsort()[-top_n:][::-1]
                concepts = [(feature_names[i], doc_vector[i]) for i in top_indices if doc_vector[i] > 0]
                concepts_by_doc[doc_idx] = concepts

            return concepts_by_doc
        except:
            # Fallback to simple keyword extraction
            return {i: self.extract_keywords(text, top_n) for i, text in enumerate(texts)}

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using simple heuristics.

        Args:
            text: Input text

        Returns:
            Dictionary with entity types and their values
        """
        entities = {
            'concepts': [],
            'actions': [],
            'attributes': []
        }

        # Extract capitalized words as potential entities (for Russian/English mixed text)
        capitalized = re.findall(r'[А-ЯЁA-Z][а-яёa-z]+', text)
        entities['concepts'].extend(capitalized)

        # Extract words that appear after common action indicators
        action_indicators = ['создать', 'построить', 'сделать', 'выстраивать', 'воспроизвести',
                           'create', 'build', 'make', 'construct', 'reproduce']

        words = text.lower().split()
        for i, word in enumerate(words):
            if any(indicator in word for indicator in action_indicators):
                if i + 1 < len(words):
                    entities['actions'].append(words[i + 1])

        # Extract adjectives and attributes (simple heuristic)
        # Words ending in common adjective suffixes
        adjective_patterns = [r'\w+ный', r'\w+кий', r'\w+ской', r'\w+ive', r'\w+al', r'\w+ful']
        for pattern in adjective_patterns:
            matches = re.findall(pattern, text.lower())
            entities['attributes'].extend(matches)

        return entities

    def detect_relationships(self, text: str) -> List[Dict[str, str]]:
        """
        Detect relationships between concepts in text.

        Args:
            text: Input text

        Returns:
            List of relationship dictionaries
        """
        relationships = []

        # Common relationship patterns
        patterns = [
            (r'(\w+)\s+(?:является|есть|это)\s+(\w+)', 'is_a'),
            (r'(\w+)\s+(?:содержит|включает|имеет)\s+(\w+)', 'has'),
            (r'(\w+)\s+(?:создает|генерирует|производит)\s+(\w+)', 'creates'),
            (r'(\w+)\s+(?:связан|связана|связано)\s+(?:с|со)\s+(\w+)', 'related_to'),
            (r'(\w+)\s+(?:через|посредством|с помощью)\s+(\w+)', 'via'),
        ]

        for pattern, rel_type in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                relationships.append({
                    'from': match.group(1),
                    'to': match.group(2),
                    'type': rel_type
                })

        return relationships

    def calculate_concept_similarity(self, concepts1: List[str], concepts2: List[str]) -> float:
        """
        Calculate similarity between two sets of concepts using Jaccard similarity.

        Args:
            concepts1: First list of concepts
            concepts2: Second list of concepts

        Returns:
            Similarity score between 0 and 1
        """
        set1 = set(concepts1)
        set2 = set(concepts2)

        if not set1 or not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def build_concept_graph(self, text: str) -> Dict:
        """
        Build a concept graph from text.

        Args:
            text: Input text

        Returns:
            Dictionary representing the concept graph
        """
        keywords = self.extract_keywords(text, top_n=15)
        entities = self.extract_entities(text)
        relationships = self.detect_relationships(text)

        # Create graph structure
        graph = {
            'nodes': [],
            'edges': []
        }

        # Add keyword nodes
        for keyword, score in keywords:
            graph['nodes'].append({
                'id': keyword,
                'type': 'keyword',
                'weight': score
            })

        # Add entity nodes
        for entity_type, entity_list in entities.items():
            for entity in entity_list[:5]:  # Limit to top 5
                if entity.lower() not in [n['id'] for n in graph['nodes']]:
                    graph['nodes'].append({
                        'id': entity.lower(),
                        'type': entity_type,
                        'weight': 0.5
                    })

        # Add relationship edges
        for rel in relationships:
            graph['edges'].append({
                'from': rel['from'],
                'to': rel['to'],
                'type': rel['type'],
                'weight': 1.0
            })

        # Add co-occurrence edges (keywords that appear together)
        words = self.preprocess_text(text)
        keyword_ids = [k[0] for k in keywords]

        for i, kw1 in enumerate(keyword_ids):
            for kw2 in keyword_ids[i+1:]:
                # Check if both keywords appear close to each other
                if kw1 in words and kw2 in words:
                    # Calculate co-occurrence score
                    kw1_positions = [j for j, w in enumerate(words) if w == kw1]
                    kw2_positions = [j for j, w in enumerate(words) if w == kw2]

                    min_distance = min(abs(p1 - p2) for p1 in kw1_positions for p2 in kw2_positions)

                    if min_distance < 10:  # Close proximity
                        weight = 1.0 / (min_distance + 1)
                        graph['edges'].append({
                            'from': kw1,
                            'to': kw2,
                            'type': 'co_occurrence',
                            'weight': weight
                        })

        return graph
