"""
Meta-Model Builder - Heuristic-based world generation
Creates meta-models and conceptual worlds from extracted concepts
Uses graph algorithms and procedural generation without LLMs
"""

import json
import math
from typing import List, Dict, Tuple, Any
from collections import defaultdict
import numpy as np


class MetaModelBuilder:
    """
    Builds meta-models and conceptual worlds using heuristic algorithms.
    Implements multidimensional space generation and concept organization.
    """

    def __init__(self, dimensions: int = 3):
        """
        Initialize the meta-model builder.

        Args:
            dimensions: Number of dimensions for the conceptual space
        """
        self.dimensions = dimensions
        self.concept_positions = {}
        self.layers = []

    def create_singularity(self, task: str, concept_graph: Dict) -> Dict:
        """
        Create a Singularity - the core semantic node.

        Args:
            task: The task or idea description
            concept_graph: Graph of extracted concepts

        Returns:
            Singularity data structure
        """
        # Calculate layers based on concept complexity
        layers_count = self._calculate_layers(concept_graph)

        # Generate visual representation
        visual_rep = self._generate_visual_representation(concept_graph)

        singularity = {
            'task': task,
            'task_vector': self._text_to_vector(task),
            'layers_count': layers_count,
            'visual_representation': visual_rep,
            'content': json.dumps(concept_graph),
            'version': 1
        }

        return singularity

    def create_points(self, concept_graph: Dict, singularity_id: int = None) -> List[Dict]:
        """
        Create Points from concept graph nodes.

        Args:
            concept_graph: Graph of extracted concepts
            singularity_id: ID of parent singularity

        Returns:
            List of Point data structures
        """
        points = []

        for node in concept_graph.get('nodes', []):
            # Generate position vector in multidimensional space
            position_vector = self._generate_position_vector(node)

            # Determine point type based on node characteristics
            point_type = self._determine_point_type(node)

            # Calculate layer based on node weight and connections
            layer = self._calculate_point_layer(node, concept_graph)

            point = {
                'task': node.get('id', ''),
                'task_vector': self._text_to_vector(node.get('id', '')),
                'position_vector': position_vector,
                'layer': layer,
                'space_dimension': self.dimensions,
                'name': node.get('id', ''),
                'content': json.dumps(node),
                'weight': node.get('weight', 1.0),
                'type': point_type,
                'is_super_cluster': node.get('weight', 0) > 0.8,
                'visual_representation': self._generate_point_visualization(node, position_vector),
                'singularity_id': singularity_id
            }

            points.append(point)
            self.concept_positions[node['id']] = position_vector

        return points

    def create_segments(self, concept_graph: Dict, points: List[Dict]) -> List[Dict]:
        """
        Create Segments (connections between Points).

        Args:
            concept_graph: Graph of extracted concepts
            points: List of created points

        Returns:
            List of Segment data structures
        """
        segments = []
        point_id_map = {p['name']: i for i, p in enumerate(points)}

        for edge in concept_graph.get('edges', []):
            from_node = edge.get('from')
            to_node = edge.get('to')

            if from_node in point_id_map and to_node in point_id_map:
                segment = {
                    'type_name': edge.get('type', 'connection'),
                    'type': self._encode_segment_type(edge.get('type', 'connection')),
                    'weight': edge.get('weight', 1.0),
                    'from_point_idx': point_id_map[from_node],
                    'to_point_idx': point_id_map[to_node]
                }
                segments.append(segment)

        return segments

    def create_space(self, space_type: str, name: str) -> Dict:
        """
        Create a Space for organizing concepts.

        Args:
            space_type: Type of space (conceptual, visual, temporal)
            name: Space name

        Returns:
            Space data structure
        """
        space_type_map = {
            'conceptual': 1,
            'visual': 2,
            'temporal': 3
        }

        space = {
            'type': space_type_map.get(space_type.lower(), 1),
            'name': name
        }

        return space

    def generate_world(self, task: str, concept_graph: Dict) -> Dict:
        """
        Generate a complete conceptual world from task and concepts.

        Args:
            task: Task description
            concept_graph: Extracted concept graph

        Returns:
            Complete world data structure
        """
        # Create the main conceptual space
        space = self.create_space('conceptual', f"World: {task[:50]}")

        # Create the central singularity
        singularity = self.create_singularity(task, concept_graph)

        # Create points from concepts
        points = self.create_points(concept_graph)

        # Create segments (connections)
        segments = self.create_segments(concept_graph, points)

        # Create objects from entities
        objects = self._create_objects_from_graph(concept_graph)

        # Create relations between objects
        relations = self._create_relations(concept_graph, objects)

        world = {
            'space': space,
            'singularity': singularity,
            'points': points,
            'segments': segments,
            'objects': objects,
            'relations': relations,
            'metadata': {
                'total_concepts': len(points),
                'total_connections': len(segments),
                'total_objects': len(objects),
                'dimensions': self.dimensions,
                'layers': singularity['layers_count']
            }
        }

        return world

    def _calculate_layers(self, concept_graph: Dict) -> int:
        """Calculate number of layers based on graph complexity."""
        num_nodes = len(concept_graph.get('nodes', []))

        if num_nodes < 5:
            return 1
        elif num_nodes < 15:
            return 2
        elif num_nodes < 30:
            return 3
        else:
            return 4

    def _generate_visual_representation(self, concept_graph: Dict) -> Dict:
        """Generate visual representation data for the concept graph."""
        return {
            'graph_structure': 'multidimensional',
            'node_count': len(concept_graph.get('nodes', [])),
            'edge_count': len(concept_graph.get('edges', [])),
            'layout': 'force_directed'
        }

    def _text_to_vector(self, text: str) -> List[float]:
        """
        Convert text to a simple heuristic vector.
        Uses character frequencies and text statistics.
        """
        if not text:
            return [0.0] * 10

        # Calculate various text features
        features = [
            len(text) / 100.0,  # Length normalized
            len(text.split()) / 20.0,  # Word count normalized
            sum(1 for c in text if c.isupper()) / max(len(text), 1),  # Capital letter ratio
            sum(1 for c in text if c.isdigit()) / max(len(text), 1),  # Digit ratio
            sum(1 for c in text if c.isspace()) / max(len(text), 1),  # Space ratio
            len(set(text.lower())) / max(len(text), 1),  # Unique char ratio
            text.count('а') / max(len(text), 1),  # Frequency of 'а'
            text.count('e') / max(len(text), 1),  # Frequency of 'e'
            hash(text) % 100 / 100.0,  # Hash-based feature
            len(text) % 10 / 10.0  # Length modulo
        ]

        return features[:10]

    def _generate_position_vector(self, node: Dict) -> List[float]:
        """
        Generate position vector for a node in multidimensional space.
        Uses heuristic placement based on node properties.
        """
        # Use hash of node ID for deterministic but distributed placement
        node_id = node.get('id', '')
        hash_value = hash(node_id)

        position = []
        for i in range(self.dimensions):
            # Generate coordinate using different hash seeds
            seed = hash_value + i * 1000
            coord = (seed % 10000) / 10000.0  # Normalize to [0, 1]

            # Apply weight influence
            weight = node.get('weight', 0.5)
            coord = coord * weight

            position.append(coord)

        return position

    def _determine_point_type(self, node: Dict) -> int:
        """
        Determine point type: 1 - resource, 2 - content, 3 - semantic
        """
        node_type = node.get('type', 'keyword')

        type_mapping = {
            'keyword': 3,  # Semantic
            'concepts': 3,  # Semantic
            'actions': 2,  # Content
            'attributes': 1  # Resource
        }

        return type_mapping.get(node_type, 3)

    def _calculate_point_layer(self, node: Dict, concept_graph: Dict) -> int:
        """Calculate layer for a point based on its connectivity."""
        node_id = node.get('id')
        edges = concept_graph.get('edges', [])

        # Count connections
        connections = sum(1 for e in edges if e.get('from') == node_id or e.get('to') == node_id)

        # Determine layer based on connectivity
        if connections == 0:
            return 0
        elif connections <= 2:
            return 1
        elif connections <= 5:
            return 2
        else:
            return 3

    def _generate_point_visualization(self, node: Dict, position: List[float]) -> Dict:
        """Generate visualization data for a point."""
        return {
            'position': position,
            'size': node.get('weight', 1.0) * 10,
            'color': self._calculate_color_from_position(position),
            'label': node.get('id', '')
        }

    def _calculate_color_from_position(self, position: List[float]) -> str:
        """Calculate color based on position in space."""
        if len(position) >= 3:
            r = int(position[0] * 255)
            g = int(position[1] * 255)
            b = int(position[2] * 255)
        else:
            r = int(position[0] * 255) if len(position) > 0 else 128
            g = int(position[0] * 128) if len(position) > 0 else 128
            b = 200
        return f"#{r:02x}{g:02x}{b:02x}"

    def _encode_segment_type(self, type_name: str) -> int:
        """Encode segment type as integer."""
        type_map = {
            'is_a': 1,
            'has': 2,
            'creates': 3,
            'related_to': 4,
            'via': 5,
            'co_occurrence': 6
        }
        return type_map.get(type_name, 0)

    def _create_objects_from_graph(self, concept_graph: Dict) -> List[Dict]:
        """Create objects from concept graph nodes."""
        objects = []

        for node in concept_graph.get('nodes', []):
            if node.get('type') in ['concepts', 'keyword']:
                obj = {
                    'is_subject': node.get('weight', 0) > 0.7,
                    'name': node.get('id', ''),
                    'type': node.get('type', 'concept'),
                    'data': node
                }
                objects.append(obj)

        return objects

    def _create_relations(self, concept_graph: Dict, objects: List[Dict]) -> List[Dict]:
        """Create relations between objects."""
        relations = []
        object_name_map = {obj['name']: i for i, obj in enumerate(objects)}

        for edge in concept_graph.get('edges', []):
            from_name = edge.get('from')
            to_name = edge.get('to')

            if from_name in object_name_map and to_name in object_name_map:
                relation = {
                    'type': edge.get('type', 'related'),
                    'from_object_idx': object_name_map[from_name],
                    'to_object_idx': object_name_map[to_name],
                    'weight': edge.get('weight', 1.0)
                }
                relations.append(relation)

        return relations
