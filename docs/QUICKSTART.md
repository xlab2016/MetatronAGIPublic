# Quick Start Guide

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/xlab2016/MetatronAGIPublic.git
cd MetatronAGIPublic
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up database (optional)**
```bash
# Create PostgreSQL database
createdb metatron_agi

# Load schema
psql metatron_agi < database/schema.sql
```

## Running Examples

### Example 1: Create Virtual World

```bash
cd examples
python create_virtual_world.py
```

This will:
- Process the idea from the GitHub issue
- Extract concepts using heuristic algorithms
- Build a meta-model
- Generate a multidimensional world
- Display visualization
- Export to JSON

### Example 2: Test Concept Extraction

```bash
cd experiments
python test_concept_extraction.py
```

This runs 5 tests:
1. Keyword extraction
2. Entity extraction
3. Relationship detection
4. Concept graph building
5. TF-IDF concept extraction

## Using the API

### Basic Usage

```python
from src.metatron_agi import MetatronAGI

# Initialize
agi = MetatronAGI(language='russian', dimensions=4)

# Process an idea
idea = """
Виртуальная реальность где AGI создаёт мир из концепций.
Пользователь погружается в этот мир через нейроинтерфейс.
"""

world = agi.process_idea(idea, save_to_db=False)

# Visualize
print(agi.visualize_world(world))
```

### With Database

```python
import os

# Set database URL
os.environ['DATABASE_URL'] = 'postgresql://user:pass@localhost/metatron_agi'

# Initialize with DB
agi = MetatronAGI(language='russian')

# Save to database
world = agi.process_idea(idea, save_to_db=True)
print(f"Saved as Singularity ID: {world['db_ids']['singularity_id']}")

# Load later
loaded = agi.load_world(world['db_ids']['singularity_id'])
```

### Custom Dimensions

```python
# Create a 5D conceptual space
agi = MetatronAGI(dimensions=5)
world = agi.process_idea(idea)

# Each point will have a 5D position vector
for point in world['points']:
    print(f"{point['name']}: {point['position_vector']}")
```

## Understanding the Output

### World Structure

```python
world = {
    'space': {
        'type': 1,  # 1=Conceptual, 2=Visual, 3=Temporal
        'name': 'World: ...'
    },
    'singularity': {
        'task': 'original idea',
        'layers_count': 3,
        'version': 1
    },
    'points': [
        {
            'name': 'концепция',
            'layer': 2,
            'weight': 0.85,
            'position_vector': [0.42, 0.73, 0.15],
            'type': 3  # 1=resource, 2=content, 3=semantic
        },
        # ...
    ],
    'segments': [
        {
            'type_name': 'creates',
            'from_point_idx': 0,
            'to_point_idx': 5,
            'weight': 1.0
        },
        # ...
    ],
    'metadata': {
        'total_concepts': 15,
        'total_connections': 23,
        'dimensions': 4
    }
}
```

### Point Types

- **Type 1 (Resource)**: Attributes and properties
- **Type 2 (Content)**: Actions and processes
- **Type 3 (Semantic)**: Core concepts and keywords

### Relationship Types

- `is_a`: Hierarchical relationships
- `has`: Possession/containment
- `creates`: Generative relationships
- `related_to`: General associations
- `via`: Instrumental relationships
- `co_occurrence`: Words appearing together

## Customization

### Add Custom Stopwords

```python
from src.concept_extractor import ConceptExtractor

extractor = ConceptExtractor(language='russian')
extractor.stopwords.add('custom_word')
```

### Adjust Extraction Parameters

```python
# Extract more keywords
keywords = extractor.extract_keywords(text, top_n=20)

# Use different TF-IDF settings
concepts = extractor.extract_concepts_tfidf(texts, top_n=10)
```

### Custom Visualization

```python
# Export to JSON for custom visualization
import json

with open('world.json', 'w', encoding='utf-8') as f:
    json.dump(world, f, indent=2, ensure_ascii=False)

# Use with visualization libraries (D3.js, Three.js, etc.)
```

## Troubleshooting

### Database Connection Issues

```python
# Check connection
from src.database_manager import DatabaseManager

db = DatabaseManager('postgresql://localhost/metatron_agi')
if db.connect():
    print("Connected!")
    db.disconnect()
else:
    print("Connection failed - check DATABASE_URL")
```

### Empty Concept Graphs

If you get few or no concepts:
- Check text language matches `language` parameter
- Try removing custom stopwords
- Increase `top_n` parameter
- Use longer input text

### Import Errors

```python
# Add src to Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
```

## Next Steps

1. Read `docs/IMPLEMENTATION.md` for technical details
2. Explore the code in `src/` directory
3. Try creating worlds with your own ideas
4. Experiment with different languages and dimensions
5. Integrate with your own applications

## Support

For issues and questions:
- GitHub Issues: https://github.com/xlab2016/MetatronAGIPublic/issues
- Email: serikzhunu@gmail.com

## Examples of Ideas to Try

### Russian
```
Умный город где все системы связаны через искусственный интеллект
Космическая станция с автономным управлением
Образовательная платформа с персонализированным обучением
```

### English
```
A smart city where all systems are connected through artificial intelligence
Space station with autonomous control
Educational platform with personalized learning
```

Happy world building! 🌍✨
