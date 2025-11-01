using System;
using System.Collections.Generic;
using System.Data;
using System.Text.Json;
using Dapper;
using Npgsql;

namespace MetatronAGI.Core
{
    /// <summary>
    /// Database Manager - PostgreSQL interface
    /// Manages database connections and operations for the Metatron AGI system
    /// </summary>
    public class DatabaseManager : IDisposable
    {
        private readonly string _connectionString;
        private NpgsqlConnection? _connection;

        public DatabaseManager(string? connectionString = null)
        {
            _connectionString = connectionString
                ?? Environment.GetEnvironmentVariable("DATABASE_URL")
                ?? "Host=localhost;Database=metatron_agi;";
        }

        public bool Connect()
        {
            try
            {
                _connection = new NpgsqlConnection(_connectionString);
                _connection.Open();
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Database connection error: {ex.Message}");
                return false;
            }
        }

        public void Disconnect()
        {
            _connection?.Close();
            _connection?.Dispose();
            _connection = null;
        }

        public void Dispose()
        {
            Disconnect();
        }

        public void ExecuteSchema(string schemaFile)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var schemaSql = System.IO.File.ReadAllText(schemaFile);
            _connection.Execute(schemaSql);
        }

        public int CreateSpace(Space spaceData)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Space (Type, Name)
                VALUES (@Type, @Name)
                RETURNING Id";

            return _connection.QuerySingle<int>(query, spaceData);
        }

        public int CreateSingularity(Singularity singularityData, int spaceId)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Singularity (Task, TaskLLMVector, LayersCount,
                                       VisualRepresentation, Content, Version, SpaceId)
                VALUES (@Task, @TaskVector::jsonb, @LayersCount,
                       @VisualRepresentation::jsonb, @Content, @Version, @SpaceId)
                RETURNING Id";

            var parameters = new
            {
                singularityData.Task,
                TaskVector = JsonSerializer.Serialize(singularityData.TaskVector),
                singularityData.LayersCount,
                VisualRepresentation = JsonSerializer.Serialize(singularityData.VisualRepresentation),
                singularityData.Content,
                singularityData.Version,
                SpaceId = spaceId
            };

            return _connection.QuerySingle<int>(query, parameters);
        }

        public int CreatePoint(Point pointData)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Point (Task, TaskLLMVector, TaskContextLLMVector, IsSuperCluster,
                                 PositionVector, Layer, QuantumTask, QuantumSpace,
                                 VisualRepresentation, SpaceDimension, Name, Content,
                                 Weight, Type, SingularityId)
                VALUES (@Task, @TaskVector::jsonb, @TaskContextVector::jsonb, @IsSuperCluster,
                       @PositionVector::jsonb, @Layer, @QuantumTask::jsonb, @QuantumSpace::jsonb,
                       @VisualRepresentation::jsonb, @SpaceDimension, @Name, @Content,
                       @Weight, @Type, @SingularityId)
                RETURNING Id";

            var parameters = new
            {
                pointData.Task,
                TaskVector = JsonSerializer.Serialize(pointData.TaskVector),
                TaskContextVector = "[]",
                pointData.IsSuperCluster,
                PositionVector = JsonSerializer.Serialize(pointData.PositionVector),
                pointData.Layer,
                QuantumTask = "{}",
                QuantumSpace = "{}",
                VisualRepresentation = JsonSerializer.Serialize(pointData.VisualRepresentation),
                pointData.SpaceDimension,
                pointData.Name,
                pointData.Content,
                pointData.Weight,
                pointData.Type,
                pointData.SingularityId
            };

            return _connection.QuerySingle<int>(query, parameters);
        }

        public int CreateSegment(Segment segmentData, int singularityId, int fromPointId, int toPointId)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Segment (TypeName, Type, Weight, SingularityId,
                                   FromPointId, ToPointId)
                VALUES (@TypeName, @Type, @Weight, @SingularityId,
                       @FromPointId, @ToPointId)
                RETURNING Id";

            var parameters = new
            {
                segmentData.TypeName,
                segmentData.Type,
                segmentData.Weight,
                SingularityId = singularityId,
                FromPointId = fromPointId,
                ToPointId = toPointId
            };

            return _connection.QuerySingle<int>(query, parameters);
        }

        public int CreateObject(WorldObject objectData, int spaceId, int? singularityId = null)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Object (IsSubject, Name, Type, Data, SingularityId, SpaceId)
                VALUES (@IsSubject, @Name, @Type, @Data::jsonb, @SingularityId, @SpaceId)
                RETURNING Id";

            var parameters = new
            {
                objectData.IsSubject,
                objectData.Name,
                objectData.Type,
                Data = JsonSerializer.Serialize(objectData.Data),
                SingularityId = singularityId,
                SpaceId = spaceId
            };

            return _connection.QuerySingle<int>(query, parameters);
        }

        public int CreateRelation(Relation relationData, int spaceId, int? singularityId,
                                 int fromObjectId, int toObjectId)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                INSERT INTO Relation (Type, SingularityId, FromObjectId,
                                    ToObjectId, SpaceId, Weight)
                VALUES (@Type, @SingularityId, @FromObjectId,
                       @ToObjectId, @SpaceId, @Weight)
                RETURNING Id";

            var parameters = new
            {
                relationData.Type,
                SingularityId = singularityId,
                FromObjectId = fromObjectId,
                ToObjectId = toObjectId,
                SpaceId = spaceId,
                relationData.Weight
            };

            return _connection.QuerySingle<int>(query, parameters);
        }

        public Dictionary<string, object> SaveWorld(World worldData)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            // Create space
            var spaceId = CreateSpace(worldData.Space);

            // Create singularity
            var singularityId = CreateSingularity(worldData.Singularity, spaceId);

            // Create points
            var pointIds = new List<int>();
            foreach (var point in worldData.Points)
            {
                point.SingularityId = singularityId;
                var pointId = CreatePoint(point);
                pointIds.Add(pointId);
            }

            // Create segments
            var segmentIds = new List<int>();
            foreach (var segment in worldData.Segments)
            {
                var fromPointId = pointIds[segment.FromPointIdx];
                var toPointId = pointIds[segment.ToPointIdx];
                var segmentId = CreateSegment(segment, singularityId, fromPointId, toPointId);
                segmentIds.Add(segmentId);
            }

            // Create objects
            var objectIds = new List<int>();
            foreach (var obj in worldData.Objects)
            {
                var objectId = CreateObject(obj, spaceId, singularityId);
                objectIds.Add(objectId);
            }

            // Create relations
            var relationIds = new List<int>();
            foreach (var relation in worldData.Relations)
            {
                var fromObjectId = objectIds[relation.FromObjectIdx];
                var toObjectId = objectIds[relation.ToObjectIdx];
                var relationId = CreateRelation(relation, spaceId, singularityId,
                                              fromObjectId, toObjectId);
                relationIds.Add(relationId);
            }

            return new Dictionary<string, object>
            {
                ["space_id"] = spaceId,
                ["singularity_id"] = singularityId,
                ["point_ids"] = pointIds,
                ["segment_ids"] = segmentIds,
                ["object_ids"] = objectIds,
                ["relation_ids"] = relationIds,
                ["metadata"] = worldData.Metadata
            };
        }

        public World? GetWorld(int singularityId)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            // Get singularity
            var singularity = _connection.QuerySingleOrDefault<dynamic>(
                "SELECT * FROM Singularity WHERE Id = @Id",
                new { Id = singularityId });

            if (singularity == null)
                return null;

            // Note: Full implementation would deserialize all related data
            // This is a simplified version
            return new World
            {
                // Would need to populate all fields from database
            };
        }

        public List<dynamic> ListWorlds(int limit = 10)
        {
            if (_connection == null)
                throw new InvalidOperationException("Not connected to database");

            var query = @"
                SELECT s.Id, s.Task, s.LayersCount, s.CreatedAt, sp.Name as SpaceName
                FROM Singularity s
                JOIN Space sp ON s.SpaceId = sp.Id
                ORDER BY s.CreatedAt DESC
                LIMIT @Limit";

            return _connection.Query<dynamic>(query, new { Limit = limit }).AsList();
        }
    }
}
