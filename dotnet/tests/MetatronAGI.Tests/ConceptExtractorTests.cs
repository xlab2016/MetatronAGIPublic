using System;
using System.Linq;
using Xunit;
using MetatronAGI.Core;

namespace MetatronAGI.Tests
{
    public class ConceptExtractorTests
    {
        [Fact]
        public void ExtractKeywords_ShouldReturnTopKeywords()
        {
            // Arrange
            var extractor = new ConceptExtractor("russian");
            var text = "AGI создает виртуальный мир из концепций. Виртуальный мир содержит множество концепций.";

            // Act
            var keywords = extractor.ExtractKeywords(text, 5);

            // Assert
            Assert.NotEmpty(keywords);
            Assert.True(keywords.Count <= 5);
            Assert.All(keywords, kw => Assert.True(kw.Score >= 0 && kw.Score <= 1));
        }

        [Fact]
        public void PreprocessText_ShouldRemoveStopwords()
        {
            // Arrange
            var extractor = new ConceptExtractor("russian");
            var text = "Это мир и концепций";

            // Act
            var words = extractor.PreprocessText(text);

            // Assert
            Assert.DoesNotContain("это", words);
            Assert.Contains("мир", words);
            Assert.Contains("концепций", words);
        }

        [Fact]
        public void BuildConceptGraph_ShouldCreateNodesAndEdges()
        {
            // Arrange
            var extractor = new ConceptExtractor("russian");
            var text = "AGI создает виртуальный мир из концепций";

            // Act
            var graph = extractor.BuildConceptGraph(text);

            // Assert
            Assert.NotEmpty(graph.Nodes);
            Assert.NotEmpty(graph.Edges);
        }

        [Fact]
        public void ExtractEntities_ShouldFindCapitalizedWords()
        {
            // Arrange
            var extractor = new ConceptExtractor("english");
            var text = "AGI creates virtual worlds using Neural interfaces";

            // Act
            var entities = extractor.ExtractEntities(text);

            // Assert
            Assert.Contains("concepts", entities.Keys);
            Assert.NotEmpty(entities["concepts"]);
        }

        [Fact]
        public void CalculateConceptSimilarity_ShouldReturnCorrectScore()
        {
            // Arrange
            var extractor = new ConceptExtractor();
            var concepts1 = new System.Collections.Generic.List<string> { "agi", "virtual", "world" };
            var concepts2 = new System.Collections.Generic.List<string> { "agi", "world", "reality" };

            // Act
            var similarity = extractor.CalculateConceptSimilarity(concepts1, concepts2);

            // Assert
            Assert.True(similarity > 0 && similarity <= 1);
        }
    }
}
