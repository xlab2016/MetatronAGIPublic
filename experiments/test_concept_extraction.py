#!/usr/bin/env python3
"""
Experiment: Test Concept Extraction
Tests the heuristic concept extraction algorithms
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from concept_extractor import ConceptExtractor


def test_keyword_extraction():
    """Test keyword extraction on sample text."""
    print("=" * 80)
    print("TEST 1: Keyword Extraction")
    print("=" * 80)

    extractor = ConceptExtractor(language='russian')

    text = """
    Искусственный интеллект создаёт виртуальные миры через нейроинтерфейс.
    Пользователь погружается в концептуальное пространство где идеи становятся реальностью.
    Метамодель строится из концепций и связей между ними.
    """

    keywords = extractor.extract_keywords(text, top_n=10)

    print(f"\nText: {text[:100]}...\n")
    print("Extracted Keywords:")
    for i, (keyword, score) in enumerate(keywords, 1):
        print(f"  {i}. {keyword} (score: {score:.3f})")
    print()


def test_entity_extraction():
    """Test entity extraction."""
    print("=" * 80)
    print("TEST 2: Entity Extraction")
    print("=" * 80)

    extractor = ConceptExtractor(language='russian')

    text = """
    AGI посредством нейроинтерфейса создаёт метамодель.
    Виртуальный мир выстраивается из семантических концепций.
    Пользователь может создать новый концептуальный объект.
    """

    entities = extractor.extract_entities(text)

    print(f"\nText: {text[:100]}...\n")
    print("Extracted Entities:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"  {entity_type.upper()}:")
            for entity in entity_list[:5]:
                print(f"    - {entity}")
    print()


def test_relationship_detection():
    """Test relationship detection."""
    print("=" * 80)
    print("TEST 3: Relationship Detection")
    print("=" * 80)

    extractor = ConceptExtractor(language='russian')

    text = """
    Интеллект создаёт модель мира.
    Концепция связана с объектом.
    Пространство содержит точки знаний.
    """

    relationships = extractor.detect_relationships(text)

    print(f"\nText: {text}\n")
    print("Detected Relationships:")
    for i, rel in enumerate(relationships, 1):
        print(f"  {i}. {rel['from']} --[{rel['type']}]--> {rel['to']}")
    print()


def test_concept_graph():
    """Test complete concept graph building."""
    print("=" * 80)
    print("TEST 4: Concept Graph Building")
    print("=" * 80)

    extractor = ConceptExtractor(language='russian')

    text = """
    Это мир высоких технологий где виртуальность интегрирована с реальностью.
    AGI создаёт метамодель из концепций и форм.
    Нейроинтерфейс позволяет погрузиться в концептуальное пространство.
    Виртуальный мир выстраивается вокруг идеи пользователя.
    """

    graph = extractor.build_concept_graph(text)

    print(f"\nText: {text[:100]}...\n")
    print(f"Graph Statistics:")
    print(f"  Nodes: {len(graph['nodes'])}")
    print(f"  Edges: {len(graph['edges'])}")
    print()

    print("Nodes:")
    for i, node in enumerate(graph['nodes'][:10], 1):
        print(f"  {i}. {node['id']} (type: {node['type']}, weight: {node['weight']:.3f})")
    print()

    print("Edges:")
    for i, edge in enumerate(graph['edges'][:10], 1):
        print(f"  {i}. {edge['from']} --[{edge['type']}]--> {edge['to']} (weight: {edge['weight']:.3f})")
    print()

    # Export to JSON
    output_file = 'concept_graph.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Graph exported to: {output_file}")
    print()


def test_tfidf_extraction():
    """Test TF-IDF concept extraction."""
    print("=" * 80)
    print("TEST 5: TF-IDF Concept Extraction")
    print("=" * 80)

    extractor = ConceptExtractor(language='russian')

    texts = [
        "Виртуальная реальность интегрирована с физическим миром через нейроинтерфейс",
        "AGI создаёт концептуальные модели из описания идей пользователя",
        "Метамодель позволяет построить целый виртуальный мир из концепций"
    ]

    concepts = extractor.extract_concepts_tfidf(texts, top_n=5)

    print("Input Texts:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")
    print()

    print("Extracted Concepts by Document:")
    for doc_idx, doc_concepts in concepts.items():
        print(f"\n  Document {doc_idx + 1}:")
        for concept, score in doc_concepts:
            print(f"    - {concept} (TF-IDF: {score:.3f})")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CONCEPT EXTRACTION TESTS" + " " * 34 + "║")
    print("║" + " " * 15 + "Heuristic-based NLP without LLM" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    test_keyword_extraction()
    test_entity_extraction()
    test_relationship_detection()
    test_concept_graph()
    test_tfidf_extraction()

    print("=" * 80)
    print("ALL TESTS COMPLETED!")
    print("=" * 80)


if __name__ == '__main__':
    main()
