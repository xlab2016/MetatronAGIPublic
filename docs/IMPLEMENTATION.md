# Metatron AGI - Heuristic Implementation

## Overview

This implementation of Metatron AGI creates conceptual worlds from user ideas using **pure heuristic algorithms** without any LLM integration. The system extracts concepts, builds meta-models, and generates multidimensional knowledge spaces using algorithmic approaches.

## Architecture

### Core Components

1. **Concept Extractor** (`src/concept_extractor.py`)
   - Keyword extraction using frequency analysis
   - TF-IDF-based concept extraction
   - Entity recognition using pattern matching
   - Relationship detection using linguistic patterns
   - Concept graph building

2. **Meta-Model Builder** (`src/metamodel_builder.py`)
   - Singularity creation (central semantic nodes)
   - Point generation (knowledge points in multidimensional space)
   - Segment creation (connections between points)
   - Space organization (conceptual, visual, temporal)
   - Procedural world generation

3. **Database Manager** (`src/database_manager.py`)
   - PostgreSQL interface following ERM model
   - CRUD operations for all entities
   - World persistence and retrieval
   - Transaction management

4. **Main AGI System** (`src/metatron_agi.py`)
   - Orchestrates all components
   - Provides high-level API
   - Interactive world exploration
   - Visualization generation

## How It Works

### Step 1: Concept Extraction

When a user provides an idea or thought, the system:

1. **Preprocesses the text**
   - Converts to lowercase
   - Tokenizes into words (supports Cyrillic and Latin)
   - Removes stopwords
   - Filters short words

2. **Extracts keywords**
   - Uses frequency analysis
   - Normalizes scores
   - Ranks by importance

3. **Identifies entities**
   - Detects capitalized words (potential concepts)
   - Finds action words (verbs)
   - Extracts attributes (adjectives)

4. **Detects relationships**
   - Pattern matching for common relationships:
     - "is_a" (является, есть)
     - "has" (содержит, имеет)
     - "creates" (создаёт, производит)
     - "related_to" (связан с)
     - "via" (через, посредством)

5. **Builds concept graph**
   - Creates nodes from keywords and entities
   - Creates edges from detected relationships
   - Adds co-occurrence edges for nearby keywords

### Step 2: Meta-Model Building

From the concept graph, the system builds a meta-model:

1. **Creates Singularity**
   - The central semantic node
   - Calculates layers based on complexity
   - Generates visual representation metadata

2. **Generates Points**
   - Each concept becomes a Point
   - Positioned in multidimensional space (default 3D or 4D)
   - Assigned to layers based on connectivity
   - Weighted by importance
   - Types: resource (1), content (2), semantic (3)
   - Super-clusters identified (high-weight nodes)

3. **Creates Segments**
   - Connections between Points
   - Preserves relationship types
   - Maintains edge weights

4. **Organizes Spaces**
   - Conceptual space (type 1)
   - Visual space (type 2)
   - Temporal space (type 3)

### Step 3: World Generation

The complete world structure includes:

- **Space**: The container for the world
- **Singularity**: The core semantic node with the original idea
- **Points**: All extracted concepts positioned in multidimensional space
- **Segments**: Connections showing relationships
- **Objects**: Entities derived from concepts
- **Relations**: Semantic relationships between objects

### Step 4: Visualization

The system can visualize the world in multiple formats:

- **Text**: Human-readable hierarchical view
- **JSON**: Machine-readable complete structure
- **Interactive**: Console-based exploration

## Heuristic Algorithms Used

### 1. Frequency Analysis
Simple word counting with stopword filtering for keyword extraction.

### 2. TF-IDF (Term Frequency-Inverse Document Frequency)
Statistical measure of word importance across multiple documents.

### 3. Pattern Matching
Regular expressions for relationship and entity detection.

### 4. Jaccard Similarity
Set-based similarity measure for concept comparison.

### 5. Hash-Based Positioning
Deterministic positioning of concepts in multidimensional space using hash functions.

### 6. Co-occurrence Analysis
Detecting concepts that appear together within a proximity window.

### 7. Graph Algorithms
Building and analyzing concept graphs using NetworkX principles.

## Database Schema

Based on the ERM model, the PostgreSQL schema includes:

- **Space**: Organizational container
- **Singularity**: Central semantic nodes
- **Point**: Knowledge points in multidimensional space
- **Segment**: Connections between points
- **Object**: Conceptual entities
- **Relation**: Relationships between objects
- **Vector**: Embeddings and vector representations
- **Resource**: Computational resources (for future use)
- **QuantumComputer**: Quantum computing resources (for future use)
- **LLMAgent**: LLM agents (for future extensibility)

## Usage Examples

### Basic World Creation

```python
from metatron_agi import MetatronAGI

# Initialize AGI
agi = MetatronAGI(language='russian', dimensions=4)

# Process an idea
idea = "AGI создаёт виртуальный мир из концепций"
world = agi.process_idea(idea, save_to_db=False)

# Visualize
print(agi.visualize_world(world))
```

### Database Integration

```python
# With database
agi = MetatronAGI(
    db_connection_string='postgresql://user:pass@localhost/metatron'
)

# Save to database
world = agi.process_idea(idea, save_to_db=True)

# Load later
loaded_world = agi.load_world(singularity_id=1)
```

### Interactive Exploration

```python
# Explore interactively
agi.explore_world_interactively(world)
```

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
  - Default: `postgresql://localhost/metatron_agi`

### Parameters

- `language`: Text processing language ('russian' or 'english')
- `dimensions`: Multidimensional space dimensions (default: 3)
- `top_n`: Number of top concepts to extract (configurable per method)

## Advantages of Heuristic Approach

1. **No External Dependencies**: No API keys or LLM services required
2. **Fast Processing**: Algorithmic processing is much faster than LLM calls
3. **Deterministic**: Same input always produces same output
4. **Transparent**: All logic is visible and auditable
5. **Offline**: Works completely offline
6. **Scalable**: Can process many ideas quickly
7. **Cost-Effective**: No API costs

## Limitations

1. **Language Understanding**: Limited to pattern matching vs. deep semantic understanding
2. **Context**: Cannot understand complex context like LLMs
3. **Creativity**: Less creative than LLM-based approaches
4. **Ambiguity**: May struggle with ambiguous or metaphorical language

## Future Enhancements

1. **Advanced NLP**: Integration with spaCy for better entity recognition
2. **Graph Algorithms**: More sophisticated graph analysis
3. **Visualization**: 3D/4D visualization with Plotly/Three.js
4. **Neural Interface Simulation**: Simulated interaction patterns
5. **Multi-modal**: Support for image/audio input processing
6. **Quantum Integration**: When quantum computing becomes accessible

## Testing

Run the experiment scripts:

```bash
# Test concept extraction
python experiments/test_concept_extraction.py

# Create example world
python examples/create_virtual_world.py
```

## Database Setup

```bash
# Create database
createdb metatron_agi

# Load schema
psql metatron_agi < database/schema.sql
```

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- `psycopg2-binary`: PostgreSQL interface
- `scikit-learn`: TF-IDF and ML algorithms
- `numpy`: Numerical operations
- `networkx`: Graph processing

## Contributing

This is a research project. Contributions welcome for:
- Better heuristic algorithms
- Improved pattern matching
- Multilingual support
- Visualization enhancements

## License

See LICENSE file in repository root.

## Author

Serik Zhunussov (serikzhunu@gmail.com)

Implementation by AI issue solver using heuristic algorithms as requested.
