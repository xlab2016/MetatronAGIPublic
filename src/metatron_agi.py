"""
Metatron AGI - Main System
Heuristic-based AGI for creating conceptual worlds from ideas
No LLM integration - pure algorithmic approach
"""

import json
from typing import Dict, Optional
from concept_extractor import ConceptExtractor
from metamodel_builder import MetaModelBuilder
from database_manager import DatabaseManager


class MetatronAGI:
    """
    Main Metatron AGI system.
    Creates conceptual worlds from user ideas using heuristic algorithms.
    """

    def __init__(self, db_connection_string: Optional[str] = None,
                 language: str = 'russian', dimensions: int = 3):
        """
        Initialize Metatron AGI system.

        Args:
            db_connection_string: PostgreSQL connection string
            language: Language for text processing
            dimensions: Number of dimensions for conceptual space
        """
        self.concept_extractor = ConceptExtractor(language=language)
        self.metamodel_builder = MetaModelBuilder(dimensions=dimensions)
        self.db_manager = DatabaseManager(db_connection_string)
        self.language = language
        self.dimensions = dimensions

    def process_idea(self, idea: str, save_to_db: bool = True) -> Dict:
        """
        Process an idea and create a conceptual world.

        This is the main method that:
        1. Extracts concepts from the idea
        2. Builds a concept graph
        3. Creates a meta-model and world
        4. Optionally saves to database

        Args:
            idea: User's idea or thought description
            save_to_db: Whether to save the world to database

        Returns:
            Dictionary containing the generated world
        """
        print(f"Processing idea: {idea[:100]}...")

        # Step 1: Extract concepts from the idea
        print("Step 1: Extracting concepts...")
        concept_graph = self.concept_extractor.build_concept_graph(idea)
        print(f"  - Extracted {len(concept_graph['nodes'])} concepts")
        print(f"  - Found {len(concept_graph['edges'])} relationships")

        # Step 2: Build meta-model and generate world
        print("Step 2: Building meta-model and generating world...")
        world = self.metamodel_builder.generate_world(idea, concept_graph)
        print(f"  - Created world with {world['metadata']['total_concepts']} concepts")
        print(f"  - Established {world['metadata']['total_connections']} connections")
        print(f"  - Generated {world['metadata']['total_objects']} objects")

        # Step 3: Save to database if requested
        if save_to_db:
            print("Step 3: Saving world to database...")
            if self.db_manager.connect():
                try:
                    db_ids = self.db_manager.save_world(world)
                    world['db_ids'] = db_ids
                    print(f"  - Saved to database (Singularity ID: {db_ids['singularity_id']})")
                except Exception as e:
                    print(f"  - Database save failed: {e}")
                    print("  - World generated but not saved to database")
                finally:
                    self.db_manager.disconnect()
            else:
                print("  - Could not connect to database")
                print("  - World generated but not saved to database")

        print("World creation complete!")
        return world

    def visualize_world(self, world: Dict, output_format: str = 'text') -> str:
        """
        Create a visualization of the generated world.

        Args:
            world: World data structure
            output_format: Output format ('text', 'json')

        Returns:
            Visualization string
        """
        if output_format == 'json':
            return json.dumps(world, indent=2, ensure_ascii=False)

        # Text visualization
        lines = []
        lines.append("=" * 80)
        lines.append("METATRON AGI - CONCEPTUAL WORLD")
        lines.append("=" * 80)
        lines.append("")

        # Task/Idea
        lines.append(f"IDEA: {world['singularity']['task']}")
        lines.append("")

        # Metadata
        meta = world['metadata']
        lines.append("WORLD STRUCTURE:")
        lines.append(f"  - Dimensions: {meta['dimensions']}D")
        lines.append(f"  - Layers: {meta['layers']}")
        lines.append(f"  - Total Concepts: {meta['total_concepts']}")
        lines.append(f"  - Total Connections: {meta['total_connections']}")
        lines.append(f"  - Total Objects: {meta['total_objects']}")
        lines.append("")

        # Concepts (Points)
        lines.append("CONCEPTS:")
        for i, point in enumerate(world['points'][:10], 1):  # Show first 10
            layer_indicator = "⭐" * (point['layer'] + 1)
            super_indicator = " [SUPER-CLUSTER]" if point['is_super_cluster'] else ""
            lines.append(f"  {i}. {point['name']}{super_indicator}")
            lines.append(f"     Layer: {layer_indicator} ({point['layer']})")
            lines.append(f"     Weight: {point['weight']:.2f}")
            lines.append(f"     Position: {[f'{x:.2f}' for x in point['position_vector']]}")
        if len(world['points']) > 10:
            lines.append(f"  ... and {len(world['points']) - 10} more concepts")
        lines.append("")

        # Connections (Segments)
        lines.append("CONNECTIONS:")
        for i, segment in enumerate(world['segments'][:10], 1):  # Show first 10
            from_point = world['points'][segment['from_point_idx']]
            to_point = world['points'][segment['to_point_idx']]
            lines.append(f"  {i}. {from_point['name']} --[{segment['type_name']}]--> {to_point['name']}")
            lines.append(f"     Weight: {segment['weight']:.2f}")
        if len(world['segments']) > 10:
            lines.append(f"  ... and {len(world['segments']) - 10} more connections")
        lines.append("")

        # Objects
        if world['objects']:
            lines.append("OBJECTS:")
            for i, obj in enumerate(world['objects'][:10], 1):
                subject_marker = "[SUBJECT]" if obj['is_subject'] else ""
                lines.append(f"  {i}. {obj['name']} {subject_marker}")
                lines.append(f"     Type: {obj['type']}")
            if len(world['objects']) > 10:
                lines.append(f"  ... and {len(world['objects']) - 10} more objects")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def load_world(self, singularity_id: int) -> Optional[Dict]:
        """
        Load a world from the database.

        Args:
            singularity_id: Singularity ID to load

        Returns:
            World data or None if not found
        """
        if self.db_manager.connect():
            try:
                world = self.db_manager.get_world(singularity_id)
                return world
            finally:
                self.db_manager.disconnect()
        return None

    def list_worlds(self, limit: int = 10):
        """
        List worlds from the database.

        Args:
            limit: Maximum number of worlds to return

        Returns:
            List of world summaries
        """
        if self.db_manager.connect():
            try:
                worlds = self.db_manager.list_worlds(limit)
                return worlds
            finally:
                self.db_manager.disconnect()
        return []

    def explore_world_interactively(self, world: Dict):
        """
        Interactive exploration of a generated world.

        Args:
            world: World data structure
        """
        print("\n" + "=" * 80)
        print("INTERACTIVE WORLD EXPLORATION")
        print("=" * 80)

        while True:
            print("\nOptions:")
            print("  1. View concept details")
            print("  2. View connections")
            print("  3. View objects")
            print("  4. Show full visualization")
            print("  5. Export to JSON")
            print("  0. Exit")

            choice = input("\nSelect option: ").strip()

            if choice == '0':
                break
            elif choice == '1':
                self._show_concept_details(world)
            elif choice == '2':
                self._show_connections(world)
            elif choice == '3':
                self._show_objects(world)
            elif choice == '4':
                print(self.visualize_world(world))
            elif choice == '5':
                filename = input("Enter filename (e.g., world.json): ").strip()
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(world, f, indent=2, ensure_ascii=False)
                print(f"World exported to {filename}")

    def _show_concept_details(self, world: Dict):
        """Show details of a specific concept."""
        print("\nConcepts:")
        for i, point in enumerate(world['points'], 1):
            print(f"  {i}. {point['name']}")

        try:
            idx = int(input("\nSelect concept number: ")) - 1
            if 0 <= idx < len(world['points']):
                point = world['points'][idx]
                print(f"\nConcept: {point['name']}")
                print(f"Layer: {point['layer']}")
                print(f"Weight: {point['weight']:.2f}")
                print(f"Type: {point['type']}")
                print(f"Super Cluster: {point['is_super_cluster']}")
                print(f"Position: {point['position_vector']}")
                print(f"Dimensions: {point['space_dimension']}D")
        except (ValueError, IndexError):
            print("Invalid selection")

    def _show_connections(self, world: Dict):
        """Show connections between concepts."""
        print("\nConnections:")
        for i, segment in enumerate(world['segments'], 1):
            from_point = world['points'][segment['from_point_idx']]
            to_point = world['points'][segment['to_point_idx']]
            print(f"  {i}. {from_point['name']} --[{segment['type_name']}]--> {to_point['name']}")

    def _show_objects(self, world: Dict):
        """Show objects in the world."""
        print("\nObjects:")
        for i, obj in enumerate(world['objects'], 1):
            subject_marker = "[SUBJECT]" if obj['is_subject'] else ""
            print(f"  {i}. {obj['name']} {subject_marker} (Type: {obj['type']})")
