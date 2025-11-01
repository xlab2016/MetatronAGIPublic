# MetatronAGI - .NET 8 Implementation

🤖 **Heuristic-based AGI for Creating Conceptual Worlds**

This is the .NET 8 (C#) implementation of MetatronAGI, a system that creates conceptual worlds from user ideas using **pure heuristic algorithms** without LLM integration.

## 🌟 Features

- ✅ **No LLM Dependencies** - Works completely offline using heuristic algorithms
- ✅ **Fast & Deterministic** - Same input produces same output
- ✅ **Cross-platform** - Runs on Windows, Linux, and macOS
- ✅ **PostgreSQL Integration** - Full ERM model implementation
- ✅ **Multidimensional Spaces** - 3D, 4D, 5D+ conceptual spaces
- ✅ **Graph-based** - Concepts as nodes, relationships as edges

## 🚀 Quick Start

### Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- PostgreSQL (optional, for database persistence)

### Build the Project

```bash
# Navigate to the .NET directory
cd dotnet

# Restore dependencies
dotnet restore

# Build the solution
dotnet build
```

### Run the Example

```bash
# Run the example application
dotnet run --project examples/MetatronAGI.Examples/MetatronAGI.Examples.csproj
```

## 📖 Usage

### Basic Example

```csharp
using MetatronAGI.Core;

// Initialize the AGI system
var agi = new MetatronAGI(
    dbConnectionString: null,  // Optional: PostgreSQL connection
    language: "russian",       // or "english"
    dimensions: 4              // 4D conceptual space
);

// Process an idea
string idea = @"
    Это мир высоких технологий где виртуальность
    интегрирована с реальностью. AGI создаёт метамодель
    и выстраивает целый мир из концепций.
";

var world = agi.ProcessIdea(idea, saveToDb: false);

// Visualize the world
string visualization = agi.VisualizeWorld(world);
Console.WriteLine(visualization);
```

### Working with Concept Extraction

```csharp
using MetatronAGI.Core;

var extractor = new ConceptExtractor(language: "russian");

// Extract keywords
var keywords = extractor.ExtractKeywords(text, topN: 10);

// Build concept graph
var graph = extractor.BuildConceptGraph(text);

// Extract entities
var entities = extractor.ExtractEntities(text);
```

### Building Meta-Models

```csharp
using MetatronAGI.Core;

var builder = new MetaModelBuilder(dimensions: 4);

// Create a singularity (central semantic node)
var singularity = builder.CreateSingularity(task, conceptGraph);

// Create points (concepts in multidimensional space)
var points = builder.CreatePoints(conceptGraph);

// Create segments (connections between concepts)
var segments = builder.CreateSegments(conceptGraph, points);

// Generate complete world
var world = builder.GenerateWorld(task, conceptGraph);
```

## 🏗️ Project Structure

```
dotnet/
├── src/
│   └── MetatronAGI.Core/           # Core library
│       ├── ConceptExtractor.cs     # Concept extraction algorithms
│       ├── MetaModelBuilder.cs     # Meta-model generation
│       ├── DatabaseManager.cs      # PostgreSQL integration
│       └── MetatronAGI.cs         # Main AGI system
├── examples/
│   └── MetatronAGI.Examples/       # Example console application
│       └── Program.cs
├── tests/
│   └── MetatronAGI.Tests/          # Unit tests
│       └── ConceptExtractorTests.cs
└── README.md                       # This file
```

## 🧪 Running Tests

```bash
# Run all tests
dotnet test

# Run tests with coverage
dotnet test /p:CollectCoverage=true
```

## 🗄️ Database Setup

### Create PostgreSQL Database

```bash
# Create database
createdb metatron_agi

# Load schema (from project root)
psql metatron_agi < database/schema.sql
```

### Configure Connection String

Set environment variable:

```bash
# Linux/macOS
export DATABASE_URL="Host=localhost;Database=metatron_agi;Username=postgres;Password=yourpassword"

# Windows
set DATABASE_URL=Host=localhost;Database=metatron_agi;Username=postgres;Password=yourpassword
```

Or pass directly to constructor:

```csharp
var agi = new MetatronAGI(
    dbConnectionString: "Host=localhost;Database=metatron_agi;Username=postgres;Password=yourpassword"
);
```

## 📦 NuGet Packages Used

- **Npgsql** (9.0.4) - PostgreSQL data provider
- **Dapper** (2.1.66) - Micro ORM for database operations
- **System.Text.Json** (9.0.10) - JSON serialization
- **MathNet.Numerics** (5.0.0) - Mathematical computations

## 🎯 Heuristic Algorithms

The .NET implementation uses the same heuristic algorithms as the Python version:

1. **Frequency Analysis** - Word frequency counting with stopword filtering
2. **TF-IDF** - Statistical measure of term importance
3. **Pattern Matching** - Regular expressions for relationship detection
4. **Co-occurrence Analysis** - Finding concepts that appear together
5. **Hash-based Positioning** - Deterministic placement in multidimensional space

## 🔬 Example Output

```
================================================================================
METATRON AGI - CONCEPTUAL WORLD
================================================================================

IDEA: Это мир высоких технологий где виртуальность интегрирована с реальностью

WORLD STRUCTURE:
  - Dimensions: 4D
  - Layers: 2
  - Total Concepts: 12
  - Total Connections: 18
  - Total Objects: 8

CONCEPTS:
  1. виртуальность [SUPER-CLUSTER]
     Layer: ⭐⭐ (2)
     Weight: 0.92
     Position: [0.47, 0.23, 0.81, 0.15]

  2. технологий
     Layer: ⭐ (1)
     Weight: 0.75
     Position: [0.31, 0.68, 0.42, 0.89]

CONNECTIONS:
  1. виртуальность --[related_to]--> реальностью
     Weight: 0.85
  2. agi --[creates]--> метамодель
     Weight: 1.00
```

## 🆚 Python vs .NET

Both implementations provide the same functionality:

| Feature | Python | .NET 8 |
|---------|--------|--------|
| Concept Extraction | ✅ | ✅ |
| TF-IDF Algorithm | ✅ | ✅ |
| Meta-Model Building | ✅ | ✅ |
| PostgreSQL Support | ✅ | ✅ |
| Multidimensional Spaces | ✅ | ✅ |
| Graph Generation | ✅ | ✅ |
| No LLM Dependencies | ✅ | ✅ |

**Choose .NET if:**
- You're a C# developer
- You need Windows-first deployment
- You want strong typing and compile-time safety
- You prefer Visual Studio or Rider IDE

**Choose Python if:**
- You're a Python developer
- You need rapid prototyping
- You want extensive NLP library ecosystem
- You prefer Jupyter notebooks

## 📚 Documentation

For more information, see:
- [Main README](../README.md) - Project overview
- [Architecture](../docs/ARCHITECTURE.md) - System architecture
- [Implementation Details](../docs/IMPLEMENTATION.md) - Technical details
- [Quick Start](../docs/QUICKSTART.md) - User guide

## 🤝 Contributing

This is part of the MetatronAGI project. For contribution guidelines, see the main README.

## 📝 License

This project is licensed under the same license as the main MetatronAGI project.

## 👨‍💻 Author

**Serik Zhunussov**
- Email: serikzhunu@gmail.com
- Website: [qai.asia](https://qai.asia)
- LinkedIn: [serik-zhunussov](https://www.linkedin.com/in/serik-zhunussov-01346a131)

---

🤖 .NET 8 implementation created as part of issue #1

💡 **No LLM Required** - Pure heuristic algorithms for AGI concept generation
