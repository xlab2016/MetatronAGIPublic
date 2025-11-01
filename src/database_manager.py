"""
Database Manager - PostgreSQL interface
Manages database connections and operations for the Metatron AGI system
"""

import os
import json
from typing import Dict, List, Any, Optional
import psycopg2
from psycopg2.extras import Json, RealDictCursor


class DatabaseManager:
    """
    Manages PostgreSQL database operations for Metatron AGI.
    Implements the ERM model schema.
    """

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database manager.

        Args:
            connection_string: PostgreSQL connection string
                             If None, reads from environment variable DATABASE_URL
        """
        self.connection_string = connection_string or os.getenv(
            'DATABASE_URL',
            'postgresql://localhost/metatron_agi'
        )
        self.connection = None

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = psycopg2.connect(self.connection_string)
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_schema(self, schema_file: str):
        """
        Execute SQL schema file.

        Args:
            schema_file: Path to SQL schema file
        """
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        with self.connection.cursor() as cursor:
            cursor.execute(schema_sql)
            self.connection.commit()

    def create_space(self, space_data: Dict) -> int:
        """
        Create a Space in the database.

        Args:
            space_data: Space data dictionary

        Returns:
            Created space ID
        """
        query = """
            INSERT INTO Space (Type, Name)
            VALUES (%s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                space_data['type'],
                space_data['name']
            ))
            space_id = cursor.fetchone()[0]
            self.connection.commit()
            return space_id

    def create_singularity(self, singularity_data: Dict, space_id: int) -> int:
        """
        Create a Singularity in the database.

        Args:
            singularity_data: Singularity data dictionary
            space_id: Parent space ID

        Returns:
            Created singularity ID
        """
        query = """
            INSERT INTO Singularity (Task, TaskLLMVector, LayersCount,
                                   VisualRepresentation, Content, Version, SpaceId)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                singularity_data['task'],
                Json(singularity_data.get('task_vector', [])),
                singularity_data.get('layers_count', 1),
                Json(singularity_data.get('visual_representation', {})),
                singularity_data.get('content', ''),
                singularity_data.get('version', 1),
                space_id
            ))
            singularity_id = cursor.fetchone()[0]
            self.connection.commit()
            return singularity_id

    def create_point(self, point_data: Dict) -> int:
        """
        Create a Point in the database.

        Args:
            point_data: Point data dictionary

        Returns:
            Created point ID
        """
        query = """
            INSERT INTO Point (Task, TaskLLMVector, TaskContextLLMVector, IsSuperCluster,
                             PositionVector, Layer, QuantumTask, QuantumSpace,
                             VisualRepresentation, SpaceDimension, Name, Content,
                             Weight, Type, SingularityId)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                point_data.get('task', ''),
                Json(point_data.get('task_vector', [])),
                Json(point_data.get('task_context_vector', [])),
                point_data.get('is_super_cluster', False),
                Json(point_data.get('position_vector', [])),
                point_data.get('layer', 0),
                Json(point_data.get('quantum_task', {})),
                Json(point_data.get('quantum_space', {})),
                Json(point_data.get('visual_representation', {})),
                point_data.get('space_dimension', 3),
                point_data.get('name', ''),
                point_data.get('content', ''),
                point_data.get('weight', 1.0),
                point_data.get('type', 3),
                point_data.get('singularity_id')
            ))
            point_id = cursor.fetchone()[0]
            self.connection.commit()
            return point_id

    def create_segment(self, segment_data: Dict, singularity_id: int,
                      from_point_id: int, to_point_id: int) -> int:
        """
        Create a Segment in the database.

        Args:
            segment_data: Segment data dictionary
            singularity_id: Parent singularity ID
            from_point_id: Source point ID
            to_point_id: Target point ID

        Returns:
            Created segment ID
        """
        query = """
            INSERT INTO Segment (TypeName, Type, Weight, SingularityId,
                               FromPointId, ToPointId)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                segment_data.get('type_name', ''),
                segment_data.get('type', 0),
                segment_data.get('weight', 1.0),
                singularity_id,
                from_point_id,
                to_point_id
            ))
            segment_id = cursor.fetchone()[0]
            self.connection.commit()
            return segment_id

    def create_object(self, object_data: Dict, space_id: int,
                     singularity_id: Optional[int] = None) -> int:
        """
        Create an Object in the database.

        Args:
            object_data: Object data dictionary
            space_id: Parent space ID
            singularity_id: Optional parent singularity ID

        Returns:
            Created object ID
        """
        query = """
            INSERT INTO Object (IsSubject, Name, Type, Data, SingularityId, SpaceId)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                object_data.get('is_subject', False),
                object_data.get('name', ''),
                object_data.get('type', ''),
                Json(object_data.get('data', {})),
                singularity_id,
                space_id
            ))
            object_id = cursor.fetchone()[0]
            self.connection.commit()
            return object_id

    def create_relation(self, relation_data: Dict, space_id: int,
                       singularity_id: Optional[int],
                       from_object_id: int, to_object_id: int) -> int:
        """
        Create a Relation in the database.

        Args:
            relation_data: Relation data dictionary
            space_id: Parent space ID
            singularity_id: Optional parent singularity ID
            from_object_id: Source object ID
            to_object_id: Target object ID

        Returns:
            Created relation ID
        """
        query = """
            INSERT INTO Relation (Type, SingularityId, FromObjectId,
                                ToObjectId, SpaceId, Weight)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                relation_data.get('type', ''),
                singularity_id,
                from_object_id,
                to_object_id,
                space_id,
                relation_data.get('weight', 1.0)
            ))
            relation_id = cursor.fetchone()[0]
            self.connection.commit()
            return relation_id

    def save_world(self, world_data: Dict) -> Dict[str, Any]:
        """
        Save complete world to database.

        Args:
            world_data: Complete world data structure

        Returns:
            Dictionary with created IDs
        """
        # Create space
        space_id = self.create_space(world_data['space'])

        # Create singularity
        singularity_id = self.create_singularity(
            world_data['singularity'],
            space_id
        )

        # Create points
        point_ids = []
        for point in world_data['points']:
            point['singularity_id'] = singularity_id
            point_id = self.create_point(point)
            point_ids.append(point_id)

        # Create segments
        segment_ids = []
        for segment in world_data['segments']:
            from_point_id = point_ids[segment['from_point_idx']]
            to_point_id = point_ids[segment['to_point_idx']]
            segment_id = self.create_segment(
                segment, singularity_id, from_point_id, to_point_id
            )
            segment_ids.append(segment_id)

        # Create objects
        object_ids = []
        for obj in world_data['objects']:
            object_id = self.create_object(obj, space_id, singularity_id)
            object_ids.append(object_id)

        # Create relations
        relation_ids = []
        for relation in world_data['relations']:
            from_object_id = object_ids[relation['from_object_idx']]
            to_object_id = object_ids[relation['to_object_idx']]
            relation_id = self.create_relation(
                relation, space_id, singularity_id,
                from_object_id, to_object_id
            )
            relation_ids.append(relation_id)

        return {
            'space_id': space_id,
            'singularity_id': singularity_id,
            'point_ids': point_ids,
            'segment_ids': segment_ids,
            'object_ids': object_ids,
            'relation_ids': relation_ids,
            'metadata': world_data['metadata']
        }

    def get_world(self, singularity_id: int) -> Optional[Dict]:
        """
        Retrieve a world from database.

        Args:
            singularity_id: Singularity ID to retrieve

        Returns:
            World data dictionary or None
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get singularity
            cursor.execute(
                "SELECT * FROM Singularity WHERE Id = %s",
                (singularity_id,)
            )
            singularity = cursor.fetchone()

            if not singularity:
                return None

            # Get space
            cursor.execute(
                "SELECT * FROM Space WHERE Id = %s",
                (singularity['spaceid'],)
            )
            space = cursor.fetchone()

            # Get points
            cursor.execute(
                "SELECT * FROM Point WHERE SingularityId = %s",
                (singularity_id,)
            )
            points = cursor.fetchall()

            # Get segments
            cursor.execute(
                "SELECT * FROM Segment WHERE SingularityId = %s",
                (singularity_id,)
            )
            segments = cursor.fetchall()

            # Get objects
            cursor.execute(
                "SELECT * FROM Object WHERE SingularityId = %s",
                (singularity_id,)
            )
            objects = cursor.fetchall()

            # Get relations
            cursor.execute(
                "SELECT * FROM Relation WHERE SingularityId = %s",
                (singularity_id,)
            )
            relations = cursor.fetchall()

            return {
                'singularity': dict(singularity),
                'space': dict(space),
                'points': [dict(p) for p in points],
                'segments': [dict(s) for s in segments],
                'objects': [dict(o) for o in objects],
                'relations': [dict(r) for r in relations]
            }

    def list_worlds(self, limit: int = 10) -> List[Dict]:
        """
        List recent worlds.

        Args:
            limit: Maximum number of worlds to return

        Returns:
            List of world summaries
        """
        query = """
            SELECT s.Id, s.Task, s.LayersCount, s.CreatedAt, sp.Name as SpaceName
            FROM Singularity s
            JOIN Space sp ON s.SpaceId = sp.Id
            ORDER BY s.CreatedAt DESC
            LIMIT %s
        """

        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]
