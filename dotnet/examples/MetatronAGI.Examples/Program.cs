using System;
using System.IO;
using System.Text.Json;
using MetatronAGI.Core;

namespace MetatronAGI.Examples
{
    /// <summary>
    /// Example: Create Virtual World from Idea
    /// Demonstrates the core functionality of Metatron AGI
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(new string('=', 80));
            Console.WriteLine("METATRON AGI - VIRTUAL WORLD CREATION");
            Console.WriteLine("Heuristic-based AGI without LLM integration");
            Console.WriteLine(new string('=', 80));
            Console.WriteLine();

            // The idea from the GitHub issue
            var ideaRussian = @"
            Это мир высоких технологий где виртуальность интегрирована с реальностью.
            Можно придумать идею или мысль или попросить AGI воспроизвести сон или то что всплыло в сознании.
            AGI посредством нейроинтерфейса прочитает это. И создаст метамодель твоего описания.
            И начнет выстраивать вокруг него целый мир из концепций и форм.
            Затем он говорит готово ты надеваешь очки с нейро интерфейсом и целиком погружаешься в мир AGI.
            ";

            // Alternative English idea for testing
            var ideaEnglish = @"
            This is a high-tech world where virtuality is integrated with reality.
            You can come up with an idea or thought or ask AGI to reproduce a dream or something that came to mind.
            AGI will read this through a neural interface and create a meta-model of your description.
            It will begin to build an entire world of concepts and forms around it.
            Then it says it's ready, you put on glasses with a neural interface and completely immerse yourself in the AGI world.
            ";

            // Initialize Metatron AGI
            Console.WriteLine("Initializing Metatron AGI...");
            var agi = new Core.MetatronAGI(
                dbConnectionString: null,  // Will use environment variable or default
                language: "russian",  // Change to "english" for English processing
                dimensions: 4  // 4D conceptual space
            );
            Console.WriteLine("AGI initialized!\n");

            // Process the idea
            Console.WriteLine("Processing your idea...");
            Console.WriteLine($"Input: {ideaRussian.Substring(0, Math.Min(100, ideaRussian.Length))}...\n");

            // Generate world (don't save to DB for this example)
            var world = agi.ProcessIdea(ideaRussian, saveToDb: false);

            Console.WriteLine("\n" + new string('=', 80));
            Console.WriteLine("WORLD GENERATED SUCCESSFULLY!");
            Console.WriteLine(new string('=', 80));
            Console.WriteLine();

            // Display visualization
            var visualization = agi.VisualizeWorld(world, outputFormat: "text");
            Console.WriteLine(visualization);

            // Show some statistics
            Console.WriteLine("\nDETAILED STATISTICS:");
            Console.WriteLine($"  - Space Type: {world.Space.Name}");
            Console.WriteLine($"  - Singularity Version: {world.Singularity.Version}");
            Console.WriteLine($"  - Concept Layers: {world.Singularity.LayersCount}");
            Console.WriteLine($"  - Dimensional Space: {world.Metadata.Dimensions}D");
            Console.WriteLine();

            // Show concept graph structure
            Console.WriteLine("CONCEPT HIERARCHY:");
            var layers = new Dictionary<int, List<string>>();
            foreach (var point in world.Points)
            {
                if (!layers.ContainsKey(point.Layer))
                    layers[point.Layer] = new List<string>();
                layers[point.Layer].Add(point.Name);
            }

            foreach (var layer in layers.Keys.OrderBy(k => k))
            {
                var conceptsList = string.Join(", ", layers[layer].Take(5));
                Console.WriteLine($"  Layer {layer}: {conceptsList}");
                if (layers[layer].Count > 5)
                {
                    Console.WriteLine($"    ... and {layers[layer].Count - 5} more");
                }
            }
            Console.WriteLine();

            // Export to JSON file
            var outputFile = "generated_world.json";
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            };
            File.WriteAllText(outputFile, JsonSerializer.Serialize(world, options));
            Console.WriteLine($"World exported to: {outputFile}");
            Console.WriteLine();

            Console.WriteLine("\nThank you for using Metatron AGI!");
            Console.WriteLine(new string('=', 80));
        }
    }
}
