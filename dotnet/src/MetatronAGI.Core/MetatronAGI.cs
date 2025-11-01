using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;

namespace MetatronAGI.Core
{
    /// <summary>
    /// Metatron AGI - Main System
    /// Heuristic-based AGI for creating conceptual worlds from ideas
    /// No LLM integration - pure algorithmic approach
    /// </summary>
    public class MetatronAGI
    {
        private readonly ConceptExtractor _conceptExtractor;
        private readonly MetaModelBuilder _metamodelBuilder;
        private readonly DatabaseManager _dbManager;
        private readonly string _language;
        private readonly int _dimensions;

        public MetatronAGI(string? dbConnectionString = null,
                          string language = "russian",
                          int dimensions = 3)
        {
            _conceptExtractor = new ConceptExtractor(language);
            _metamodelBuilder = new MetaModelBuilder(dimensions);
            _dbManager = new DatabaseManager(dbConnectionString);
            _language = language;
            _dimensions = dimensions;
        }

        /// <summary>
        /// Process an idea and create a conceptual world.
        /// This is the main method that:
        /// 1. Extracts concepts from the idea
        /// 2. Builds a concept graph
        /// 3. Creates a meta-model and world
        /// 4. Optionally saves to database
        /// </summary>
        public World ProcessIdea(string idea, bool saveToDb = true)
        {
            Console.WriteLine($"Processing idea: {idea.Substring(0, Math.Min(100, idea.Length))}...");

            // Step 1: Extract concepts from the idea
            Console.WriteLine("Step 1: Extracting concepts...");
            var conceptGraph = _conceptExtractor.BuildConceptGraph(idea);
            Console.WriteLine($"  - Extracted {conceptGraph.Nodes.Count} concepts");
            Console.WriteLine($"  - Found {conceptGraph.Edges.Count} relationships");

            // Step 2: Build meta-model and generate world
            Console.WriteLine("Step 2: Building meta-model and generating world...");
            var world = _metamodelBuilder.GenerateWorld(idea, conceptGraph);
            Console.WriteLine($"  - Created world with {world.Metadata.TotalConcepts} concepts");
            Console.WriteLine($"  - Established {world.Metadata.TotalConnections} connections");
            Console.WriteLine($"  - Generated {world.Metadata.TotalObjects} objects");

            // Step 3: Save to database if requested
            if (saveToDb)
            {
                Console.WriteLine("Step 3: Saving world to database...");
                if (_dbManager.Connect())
                {
                    try
                    {
                        var dbIds = _dbManager.SaveWorld(world);
                        Console.WriteLine($"  - Saved to database (Singularity ID: {dbIds["singularity_id"]})");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"  - Database save failed: {ex.Message}");
                        Console.WriteLine("  - World generated but not saved to database");
                    }
                    finally
                    {
                        _dbManager.Disconnect();
                    }
                }
                else
                {
                    Console.WriteLine("  - Could not connect to database");
                    Console.WriteLine("  - World generated but not saved to database");
                }
            }

            Console.WriteLine("World creation complete!");
            return world;
        }

        /// <summary>
        /// Create a visualization of the generated world.
        /// </summary>
        public string VisualizeWorld(World world, string outputFormat = "text")
        {
            if (outputFormat == "json")
            {
                return JsonSerializer.Serialize(world, new JsonSerializerOptions
                {
                    WriteIndented = true,
                    Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
                });
            }

            // Text visualization
            var sb = new StringBuilder();
            sb.AppendLine(new string('=', 80));
            sb.AppendLine("METATRON AGI - CONCEPTUAL WORLD");
            sb.AppendLine(new string('=', 80));
            sb.AppendLine();

            // Task/Idea
            sb.AppendLine($"IDEA: {world.Singularity.Task}");
            sb.AppendLine();

            // Metadata
            var meta = world.Metadata;
            sb.AppendLine("WORLD STRUCTURE:");
            sb.AppendLine($"  - Dimensions: {meta.Dimensions}D");
            sb.AppendLine($"  - Layers: {meta.Layers}");
            sb.AppendLine($"  - Total Concepts: {meta.TotalConcepts}");
            sb.AppendLine($"  - Total Connections: {meta.TotalConnections}");
            sb.AppendLine($"  - Total Objects: {meta.TotalObjects}");
            sb.AppendLine();

            // Concepts (Points)
            sb.AppendLine("CONCEPTS:");
            var pointsToShow = world.Points.Take(10).ToList();
            for (int i = 0; i < pointsToShow.Count; i++)
            {
                var point = pointsToShow[i];
                var layerIndicator = new string('⭐', point.Layer + 1);
                var superIndicator = point.IsSuperCluster ? " [SUPER-CLUSTER]" : "";
                sb.AppendLine($"  {i + 1}. {point.Name}{superIndicator}");
                sb.AppendLine($"     Layer: {layerIndicator} ({point.Layer})");
                sb.AppendLine($"     Weight: {point.Weight:F2}");
                sb.AppendLine($"     Position: [{string.Join(", ", point.PositionVector.Select(x => x.ToString("F2")))}]");
            }
            if (world.Points.Count > 10)
            {
                sb.AppendLine($"  ... and {world.Points.Count - 10} more concepts");
            }
            sb.AppendLine();

            // Connections (Segments)
            sb.AppendLine("CONNECTIONS:");
            var segmentsToShow = world.Segments.Take(10).ToList();
            for (int i = 0; i < segmentsToShow.Count; i++)
            {
                var segment = segmentsToShow[i];
                var fromPoint = world.Points[segment.FromPointIdx];
                var toPoint = world.Points[segment.ToPointIdx];
                sb.AppendLine($"  {i + 1}. {fromPoint.Name} --[{segment.TypeName}]--> {toPoint.Name}");
                sb.AppendLine($"     Weight: {segment.Weight:F2}");
            }
            if (world.Segments.Count > 10)
            {
                sb.AppendLine($"  ... and {world.Segments.Count - 10} more connections");
            }
            sb.AppendLine();

            // Objects
            if (world.Objects.Any())
            {
                sb.AppendLine("OBJECTS:");
                var objectsToShow = world.Objects.Take(10).ToList();
                for (int i = 0; i < objectsToShow.Count; i++)
                {
                    var obj = objectsToShow[i];
                    var subjectMarker = obj.IsSubject ? "[SUBJECT]" : "";
                    sb.AppendLine($"  {i + 1}. {obj.Name} {subjectMarker}");
                    sb.AppendLine($"     Type: {obj.Type}");
                }
                if (world.Objects.Count > 10)
                {
                    sb.AppendLine($"  ... and {world.Objects.Count - 10} more objects");
                }
                sb.AppendLine();
            }

            sb.AppendLine(new string('=', 80));

            return sb.ToString();
        }

        /// <summary>
        /// Load a world from the database.
        /// </summary>
        public World? LoadWorld(int singularityId)
        {
            if (_dbManager.Connect())
            {
                try
                {
                    return _dbManager.GetWorld(singularityId);
                }
                finally
                {
                    _dbManager.Disconnect();
                }
            }
            return null;
        }

        /// <summary>
        /// List worlds from the database.
        /// </summary>
        public List<dynamic> ListWorlds(int limit = 10)
        {
            if (_dbManager.Connect())
            {
                try
                {
                    return _dbManager.ListWorlds(limit);
                }
                finally
                {
                    _dbManager.Disconnect();
                }
            }
            return new List<dynamic>();
        }
    }
}
