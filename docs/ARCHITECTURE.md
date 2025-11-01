# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Metatron AGI System                      │
│                  (Heuristic Implementation)                 │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │     User Input (Idea/Thought)          │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │      Concept Extractor                 │
        │  • Keyword extraction                  │
        │  • Entity recognition                  │
        │  • Relationship detection              │
        │  • TF-IDF analysis                     │
        │  • Co-occurrence analysis              │
        └────────────────────────────────────────┘
                             │
                             ▼
                    [Concept Graph]
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │      Meta-Model Builder                │
        │  • Singularity creation                │
        │  • Point generation (N-D space)        │
        │  • Segment creation                    │
        │  • Space organization                  │
        │  • Object/Relation mapping             │
        └────────────────────────────────────────┘
                             │
                             ▼
                    [World Structure]
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │      Database Manager                  │
        │  • PostgreSQL interface                │
        │  • ERM model implementation            │
        │  • CRUD operations                     │
        │  • Transaction management              │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │      PostgreSQL Database               │
        │  • Spaces, Singularities               │
        │  • Points, Segments                    │
        │  • Objects, Relations                  │
        │  • Vectors                             │
        └────────────────────────────────────────┘
```

## Component Details

### 1. Concept Extractor

**Purpose**: Extract meaningful concepts from text without using LLMs.

**Methods**:
- `preprocess_text()`: Tokenization and stopword removal
- `extract_keywords()`: Frequency-based keyword extraction
- `extract_concepts_tfidf()`: TF-IDF based concept extraction
- `extract_entities()`: Pattern-based entity recognition
- `detect_relationships()`: Linguistic pattern matching
- `build_concept_graph()`: Complete graph construction

**Algorithms**:
- Word frequency analysis
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Regular expression patterns for relationships
- Co-occurrence detection within proximity windows
- Jaccard similarity for concept comparison

### 2. Meta-Model Builder

**Purpose**: Transform concept graphs into multidimensional world structures.

**Methods**:
- `create_singularity()`: Central semantic node creation
- `create_points()`: Concept positioning in N-D space
- `create_segments()`: Relationship mapping
- `create_space()`: Space organization
- `generate_world()`: Complete world assembly

**Algorithms**:
- Hash-based deterministic positioning
- Layer calculation based on connectivity
- Weight-based importance scoring
- Graph traversal for structure analysis

### 3. Database Manager

**Purpose**: Persist and retrieve world structures in PostgreSQL.

**Methods**:
- `connect()`, `disconnect()`: Connection management
- `create_space()`, `create_singularity()`: Entity creation
- `create_point()`, `create_segment()`: Graph element storage
- `save_world()`: Complete world persistence
- `get_world()`, `list_worlds()`: World retrieval

**Features**:
- Transaction support
- JSONB for complex data structures
- Indexed queries for performance
- Automatic timestamp management

### 4. Main AGI System

**Purpose**: Orchestrate all components and provide user interface.

**Methods**:
- `process_idea()`: Main processing pipeline
- `visualize_world()`: Text and JSON visualization
- `explore_world_interactively()`: Interactive exploration
- `load_world()`, `list_worlds()`: Database access

## Data Flow

1. **Input**: User provides text description (idea/thought)
2. **Preprocessing**: Text is cleaned, tokenized, stopwords removed
3. **Extraction**: Concepts, entities, and relationships extracted
4. **Graph Building**: Concept graph constructed with nodes and edges
5. **Meta-Model Creation**: Graph transformed into multidimensional structure
6. **World Generation**: Complete world with all entities created
7. **Persistence**: World saved to database (optional)
8. **Visualization**: World displayed to user

## Data Structures

### Concept Graph
```python
{
    'nodes': [
        {
            'id': 'concept_name',
            'type': 'keyword|concepts|actions|attributes',
            'weight': float  # 0.0-1.0
        }
    ],
    'edges': [
        {
            'from': 'concept1',
            'to': 'concept2',
            'type': 'is_a|has|creates|related_to|via|co_occurrence',
            'weight': float
        }
    ]
}
```

### World Structure
```python
{
    'space': {
        'type': int,  # 1=Conceptual, 2=Visual, 3=Temporal
        'name': str
    },
    'singularity': {
        'task': str,
        'task_vector': [float],
        'layers_count': int,
        'visual_representation': dict,
        'content': str,
        'version': int
    },
    'points': [
        {
            'name': str,
            'position_vector': [float],  # N-dimensional
            'layer': int,
            'weight': float,
            'type': int,  # 1=resource, 2=content, 3=semantic
            'is_super_cluster': bool
        }
    ],
    'segments': [
        {
            'type_name': str,
            'type': int,
            'weight': float,
            'from_point_idx': int,
            'to_point_idx': int
        }
    ],
    'objects': [...],
    'relations': [...],
    'metadata': {
        'total_concepts': int,
        'total_connections': int,
        'total_objects': int,
        'dimensions': int,
        'layers': int
    }
}
```

## Multidimensional Space

Concepts are positioned in N-dimensional space (default 3D or 4D):

- **Dimension 1-3**: Spatial positioning based on concept hash
- **Dimension 4+**: Additional semantic dimensions
- **Position calculation**: Deterministic hash-based for reproducibility
- **Weight influence**: High-weight concepts positioned more prominently

## Layer System

Concepts are organized in layers based on connectivity:

- **Layer 0**: Isolated concepts (no connections)
- **Layer 1**: Basic connections (1-2 edges)
- **Layer 2**: Well-connected (3-5 edges)
- **Layer 3+**: Highly connected hub nodes (6+ edges)

## Type System

### Point Types
- **Type 1 (Resource)**: Attributes, properties, resources
- **Type 2 (Content)**: Actions, processes, operations
- **Type 3 (Semantic)**: Core concepts, keywords, entities

### Relationship Types
- **is_a**: Hierarchical classification
- **has**: Containment or possession
- **creates**: Generative relationship
- **related_to**: General association
- **via**: Instrumental relationship
- **co_occurrence**: Statistical co-location

### Space Types
- **Type 1 (Conceptual)**: Abstract concept organization
- **Type 2 (Visual)**: Visual/spatial representation
- **Type 3 (Temporal)**: Time-based organization

## Extensibility

The architecture supports future enhancements:

1. **LLM Integration**: Can add LLM-based concept extraction alongside heuristics
2. **Quantum Computing**: Prepared structures for quantum processing
3. **Neural Interfaces**: Data structures ready for brain-computer interface
4. **Distributed Processing**: Singularities can be distributed across nodes
5. **Real-time Updates**: Database supports dynamic world evolution

## Performance Considerations

- **Memory**: Concept graphs kept in memory during processing
- **Database**: Indexed queries for fast retrieval
- **Scalability**: Can process multiple ideas in parallel
- **Caching**: Concept positions cached to avoid recalculation

## Security

- **SQL Injection**: Using parameterized queries
- **Data Validation**: Type checking on all inputs
- **Connection Management**: Proper connection pooling
- **Error Handling**: Graceful degradation on failures
