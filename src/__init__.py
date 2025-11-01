"""
Metatron AGI - Heuristic Implementation
No LLM integration - pure algorithmic approach
"""

from .concept_extractor import ConceptExtractor
from .metamodel_builder import MetaModelBuilder
from .database_manager import DatabaseManager
from .metatron_agi import MetatronAGI

__version__ = '0.1.0'
__all__ = [
    'ConceptExtractor',
    'MetaModelBuilder',
    'DatabaseManager',
    'MetatronAGI'
]
