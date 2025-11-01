using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace MetatronAGI.Core
{
    /// <summary>
    /// Meta-Model Builder - Heuristic-based world generation
    /// Creates meta-models and conceptual worlds from extracted concepts
    /// Uses graph algorithms and procedural generation without LLMs
    /// </summary>
    public class MetaModelBuilder
    {
        private readonly int _dimensions;
        private readonly Dictionary<string, List<double>> _conceptPositions;
        private readonly List<int> _layers;

        public MetaModelBuilder(int dimensions = 3)
        {
            _dimensions = dimensions;
            _conceptPositions = new Dictionary<string, List<double>>();
            _layers = new List<int>();
        }

        public Singularity CreateSingularity(string task, ConceptGraph conceptGraph)
        {
            // Calculate layers based on concept complexity
            var layersCount = CalculateLayers(conceptGraph);

            // Generate visual representation
            var visualRep = GenerateVisualRepresentation(conceptGraph);

            return new Singularity
            {
                Task = task,
                TaskVector = TextToVector(task),
                LayersCount = layersCount,
                VisualRepresentation = visualRep,
                Content = JsonSerializer.Serialize(conceptGraph),
                Version = 1
            };
        }

        public List<Point> CreatePoints(ConceptGraph conceptGraph, int? singularityId = null)
        {
            var points = new List<Point>();

            foreach (var node in conceptGraph.Nodes)
            {
                // Generate position vector in multidimensional space
                var positionVector = GeneratePositionVector(node);

                // Determine point type based on node characteristics
                var pointType = DeterminePointType(node);

                // Calculate layer based on node weight and connections
                var layer = CalculatePointLayer(node, conceptGraph);

                var point = new Point
                {
                    Task = node.Id,
                    TaskVector = TextToVector(node.Id),
                    PositionVector = positionVector,
                    Layer = layer,
                    SpaceDimension = _dimensions,
                    Name = node.Id,
                    Content = JsonSerializer.Serialize(node),
                    Weight = node.Weight,
                    Type = pointType,
                    IsSuperCluster = node.Weight > 0.8,
                    VisualRepresentation = GeneratePointVisualization(node, positionVector),
                    SingularityId = singularityId
                };

                points.Add(point);
                _conceptPositions[node.Id] = positionVector;
            }

            return points;
        }

        public List<Segment> CreateSegments(ConceptGraph conceptGraph, List<Point> points)
        {
            var segments = new List<Segment>();
            var pointIdMap = points.Select((p, i) => new { p.Name, Index = i })
                                  .ToDictionary(x => x.Name, x => x.Index);

            foreach (var edge in conceptGraph.Edges)
            {
                if (pointIdMap.ContainsKey(edge.From) && pointIdMap.ContainsKey(edge.To))
                {
                    segments.Add(new Segment
                    {
                        TypeName = edge.Type,
                        Type = EncodeSegmentType(edge.Type),
                        Weight = edge.Weight,
                        FromPointIdx = pointIdMap[edge.From],
                        ToPointIdx = pointIdMap[edge.To]
                    });
                }
            }

            return segments;
        }

        public Space CreateSpace(string spaceType, string name)
        {
            var spaceTypeMap = new Dictionary<string, int>
            {
                ["conceptual"] = 1,
                ["visual"] = 2,
                ["temporal"] = 3
            };

            return new Space
            {
                Type = spaceTypeMap.ContainsKey(spaceType.ToLower())
                    ? spaceTypeMap[spaceType.ToLower()]
                    : 1,
                Name = name
            };
        }

        public World GenerateWorld(string task, ConceptGraph conceptGraph)
        {
            // Create the main conceptual space
            var space = CreateSpace("conceptual", $"World: {task.Substring(0, Math.Min(50, task.Length))}");

            // Create the central singularity
            var singularity = CreateSingularity(task, conceptGraph);

            // Create points from concepts
            var points = CreatePoints(conceptGraph);

            // Create segments (connections)
            var segments = CreateSegments(conceptGraph, points);

            // Create objects from entities
            var objects = CreateObjectsFromGraph(conceptGraph);

            // Create relations between objects
            var relations = CreateRelations(conceptGraph, objects);

            return new World
            {
                Space = space,
                Singularity = singularity,
                Points = points,
                Segments = segments,
                Objects = objects,
                Relations = relations,
                Metadata = new WorldMetadata
                {
                    TotalConcepts = points.Count,
                    TotalConnections = segments.Count,
                    TotalObjects = objects.Count,
                    Dimensions = _dimensions,
                    Layers = singularity.LayersCount
                }
            };
        }

        private int CalculateLayers(ConceptGraph conceptGraph)
        {
            var numNodes = conceptGraph.Nodes.Count;

            if (numNodes < 5) return 1;
            if (numNodes < 15) return 2;
            if (numNodes < 30) return 3;
            return 4;
        }

        private Dictionary<string, object> GenerateVisualRepresentation(ConceptGraph conceptGraph)
        {
            return new Dictionary<string, object>
            {
                ["graph_structure"] = "multidimensional",
                ["node_count"] = conceptGraph.Nodes.Count,
                ["edge_count"] = conceptGraph.Edges.Count,
                ["layout"] = "force_directed"
            };
        }

        private List<double> TextToVector(string text)
        {
            if (string.IsNullOrEmpty(text))
                return Enumerable.Repeat(0.0, 10).ToList();

            var features = new List<double>
            {
                text.Length / 100.0,
                text.Split().Length / 20.0,
                text.Count(c => char.IsUpper(c)) / (double)Math.Max(text.Length, 1),
                text.Count(c => char.IsDigit(c)) / (double)Math.Max(text.Length, 1),
                text.Count(c => char.IsWhiteSpace(c)) / (double)Math.Max(text.Length, 1),
                text.ToLower().Distinct().Count() / (double)Math.Max(text.Length, 1),
                text.Count(c => c == 'а') / (double)Math.Max(text.Length, 1),
                text.Count(c => c == 'e') / (double)Math.Max(text.Length, 1),
                (text.GetHashCode() % 100) / 100.0,
                (text.Length % 10) / 10.0
            };

            return features.Take(10).ToList();
        }

        private List<double> GeneratePositionVector(ConceptNode node)
        {
            var nodeId = node.Id;
            var hashValue = nodeId.GetHashCode();
            var position = new List<double>();

            for (int i = 0; i < _dimensions; i++)
            {
                var seed = hashValue + i * 1000;
                var coord = (Math.Abs(seed % 10000)) / 10000.0;

                // Apply weight influence
                coord *= node.Weight;

                position.Add(coord);
            }

            return position;
        }

        private int DeterminePointType(ConceptNode node)
        {
            var typeMapping = new Dictionary<string, int>
            {
                ["keyword"] = 3,
                ["concepts"] = 3,
                ["actions"] = 2,
                ["attributes"] = 1
            };

            return typeMapping.ContainsKey(node.Type) ? typeMapping[node.Type] : 3;
        }

        private int CalculatePointLayer(ConceptNode node, ConceptGraph conceptGraph)
        {
            var nodeId = node.Id;
            var connections = conceptGraph.Edges.Count(e => e.From == nodeId || e.To == nodeId);

            if (connections == 0) return 0;
            if (connections <= 2) return 1;
            if (connections <= 5) return 2;
            return 3;
        }

        private Dictionary<string, object> GeneratePointVisualization(ConceptNode node, List<double> position)
        {
            return new Dictionary<string, object>
            {
                ["position"] = position,
                ["size"] = node.Weight * 10,
                ["color"] = CalculateColorFromPosition(position),
                ["label"] = node.Id
            };
        }

        private string CalculateColorFromPosition(List<double> position)
        {
            int r, g, b;

            if (position.Count >= 3)
            {
                r = (int)(position[0] * 255);
                g = (int)(position[1] * 255);
                b = (int)(position[2] * 255);
            }
            else
            {
                r = position.Count > 0 ? (int)(position[0] * 255) : 128;
                g = position.Count > 0 ? (int)(position[0] * 128) : 128;
                b = 200;
            }

            return $"#{r:X2}{g:X2}{b:X2}";
        }

        private int EncodeSegmentType(string typeName)
        {
            var typeMap = new Dictionary<string, int>
            {
                ["is_a"] = 1,
                ["has"] = 2,
                ["creates"] = 3,
                ["related_to"] = 4,
                ["via"] = 5,
                ["co_occurrence"] = 6
            };

            return typeMap.ContainsKey(typeName) ? typeMap[typeName] : 0;
        }

        private List<WorldObject> CreateObjectsFromGraph(ConceptGraph conceptGraph)
        {
            var objects = new List<WorldObject>();

            foreach (var node in conceptGraph.Nodes)
            {
                if (node.Type == "concepts" || node.Type == "keyword")
                {
                    objects.Add(new WorldObject
                    {
                        IsSubject = node.Weight > 0.7,
                        Name = node.Id,
                        Type = node.Type,
                        Data = node
                    });
                }
            }

            return objects;
        }

        private List<Relation> CreateRelations(ConceptGraph conceptGraph, List<WorldObject> objects)
        {
            var relations = new List<Relation>();
            var objectNameMap = objects.Select((obj, i) => new { obj.Name, Index = i })
                                      .ToDictionary(x => x.Name, x => x.Index);

            foreach (var edge in conceptGraph.Edges)
            {
                if (objectNameMap.ContainsKey(edge.From) && objectNameMap.ContainsKey(edge.To))
                {
                    relations.Add(new Relation
                    {
                        Type = edge.Type,
                        FromObjectIdx = objectNameMap[edge.From],
                        ToObjectIdx = objectNameMap[edge.To],
                        Weight = edge.Weight
                    });
                }
            }

            return relations;
        }
    }

    // Data models
    public class Singularity
    {
        public string Task { get; set; } = string.Empty;
        public List<double> TaskVector { get; set; } = new List<double>();
        public int LayersCount { get; set; }
        public Dictionary<string, object> VisualRepresentation { get; set; } = new Dictionary<string, object>();
        public string Content { get; set; } = string.Empty;
        public int Version { get; set; }
    }

    public class Point
    {
        public string Task { get; set; } = string.Empty;
        public List<double> TaskVector { get; set; } = new List<double>();
        public List<double> PositionVector { get; set; } = new List<double>();
        public int Layer { get; set; }
        public int SpaceDimension { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public double Weight { get; set; }
        public int Type { get; set; }
        public bool IsSuperCluster { get; set; }
        public Dictionary<string, object> VisualRepresentation { get; set; } = new Dictionary<string, object>();
        public int? SingularityId { get; set; }
    }

    public class Segment
    {
        public string TypeName { get; set; } = string.Empty;
        public int Type { get; set; }
        public double Weight { get; set; }
        public int FromPointIdx { get; set; }
        public int ToPointIdx { get; set; }
    }

    public class Space
    {
        public int Type { get; set; }
        public string Name { get; set; } = string.Empty;
    }

    public class WorldObject
    {
        public bool IsSubject { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public object Data { get; set; } = new object();
    }

    public class Relation
    {
        public string Type { get; set; } = string.Empty;
        public int FromObjectIdx { get; set; }
        public int ToObjectIdx { get; set; }
        public double Weight { get; set; }
    }

    public class World
    {
        public Space Space { get; set; } = new Space();
        public Singularity Singularity { get; set; } = new Singularity();
        public List<Point> Points { get; set; } = new List<Point>();
        public List<Segment> Segments { get; set; } = new List<Segment>();
        public List<WorldObject> Objects { get; set; } = new List<WorldObject>();
        public List<Relation> Relations { get; set; } = new List<Relation>();
        public WorldMetadata Metadata { get; set; } = new WorldMetadata();
    }

    public class WorldMetadata
    {
        public int TotalConcepts { get; set; }
        public int TotalConnections { get; set; }
        public int TotalObjects { get; set; }
        public int Dimensions { get; set; }
        public int Layers { get; set; }
    }
}
