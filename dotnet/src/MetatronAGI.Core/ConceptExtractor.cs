using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace MetatronAGI.Core
{
    /// <summary>
    /// Concept Extractor - Heuristic-based NLP module
    /// Extracts concepts, entities, and relationships from text without using LLMs
    /// Uses TF-IDF, frequency analysis, and NLP techniques
    /// </summary>
    public class ConceptExtractor
    {
        private readonly string _language;
        private readonly HashSet<string> _stopwords;
        private readonly Dictionary<string, object> _conceptCache;

        public ConceptExtractor(string language = "russian")
        {
            _language = language;
            _stopwords = LoadStopwords();
            _conceptCache = new Dictionary<string, object>();
        }

        private HashSet<string> LoadStopwords()
        {
            // Basic Russian stopwords
            var russianStopwords = new HashSet<string>
            {
                "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как",
                "а", "то", "все", "она", "так", "его", "но", "да", "ты", "к", "это",
                "у", "же", "вы", "за", "бы", "по", "только", "ее", "мне", "было",
                "вот", "от", "меня", "еще", "нет", "о", "из", "ему", "теперь",
                "когда", "даже", "ну", "вдруг", "ли", "если", "уже", "или", "ни",
                "быть", "был", "него", "до", "вас", "нибудь", "опять", "уж", "вам",
                "ведь", "там", "потом", "себя", "ничего", "ей", "может", "они",
                "тут", "где", "есть", "надо", "ней", "для", "мы", "тебя", "их",
                "чем", "была", "сам", "чтоб", "без", "будто", "чего", "раз", "тоже",
                "себе", "под", "будет", "ж", "тогда", "кто", "этот", "того", "потому",
                "этого", "какой", "совсем", "ним", "здесь", "этом", "один", "почти",
                "мой", "тем", "чтобы", "нее", "сейчас", "были", "куда", "зачем",
                "всех", "никогда", "можно", "при", "наконец", "два", "об", "другой",
                "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про",
                "всего", "них", "какая", "много", "разве", "три", "эту", "моя", "впрочем",
                "хорошо", "свою", "этой", "перед", "иногда", "лучше", "чуть", "том"
            };

            // Basic English stopwords
            var englishStopwords = new HashSet<string>
            {
                "the", "is", "at", "which", "on", "a", "an", "as", "are", "was",
                "were", "been", "be", "have", "has", "had", "do", "does", "did",
                "will", "would", "should", "could", "may", "might", "must", "can",
                "and", "or", "but", "if", "then", "else", "when", "where", "why",
                "how", "all", "each", "every", "both", "few", "more", "most", "other",
                "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                "than", "too", "very", "of", "in", "to", "for", "with", "from", "by"
            };

            return _language == "russian" ? russianStopwords : englishStopwords;
        }

        public List<string> PreprocessText(string text)
        {
            // Lowercase
            text = text.ToLower();

            // Extract words (Cyrillic + Latin)
            var matches = Regex.Matches(text, @"[а-яёa-z]+");
            var words = matches.Cast<Match>().Select(m => m.Value).ToList();

            // Remove stopwords and short words
            return words.Where(w => !_stopwords.Contains(w) && w.Length > 2).ToList();
        }

        public List<(string Keyword, double Score)> ExtractKeywords(string text, int topN = 10)
        {
            var words = PreprocessText(text);

            // Count word frequencies
            var wordFreq = new Dictionary<string, int>();
            foreach (var word in words)
            {
                if (!wordFreq.ContainsKey(word))
                    wordFreq[word] = 0;
                wordFreq[word]++;
            }

            if (wordFreq.Count == 0)
                return new List<(string, double)>();

            // Normalize scores
            var maxFreq = wordFreq.Values.Max();
            return wordFreq
                .OrderByDescending(kvp => kvp.Value)
                .Take(topN)
                .Select(kvp => (kvp.Key, (double)kvp.Value / maxFreq))
                .ToList();
        }

        public Dictionary<int, List<(string Concept, double Score)>> ExtractConceptsTfidf(
            List<string> texts, int topN = 5)
        {
            if (texts == null || texts.Count == 0)
                return new Dictionary<int, List<(string, double)>>();

            try
            {
                // Simplified TF-IDF implementation
                var result = new Dictionary<int, List<(string, double)>>();

                // Calculate term frequencies for each document
                var docTermFreqs = new List<Dictionary<string, int>>();
                var allTerms = new HashSet<string>();

                foreach (var text in texts)
                {
                    var terms = PreprocessText(text);
                    var termFreq = new Dictionary<string, int>();

                    foreach (var term in terms)
                    {
                        if (!termFreq.ContainsKey(term))
                            termFreq[term] = 0;
                        termFreq[term]++;
                        allTerms.Add(term);
                    }

                    docTermFreqs.Add(termFreq);
                }

                // Calculate IDF for each term
                var idf = new Dictionary<string, double>();
                foreach (var term in allTerms)
                {
                    var docsWithTerm = docTermFreqs.Count(d => d.ContainsKey(term));
                    idf[term] = Math.Log((double)texts.Count / (1 + docsWithTerm));
                }

                // Calculate TF-IDF scores for each document
                for (int docIdx = 0; docIdx < texts.Count; docIdx++)
                {
                    var termFreq = docTermFreqs[docIdx];
                    var maxFreq = termFreq.Count > 0 ? termFreq.Values.Max() : 1;

                    var tfidfScores = new List<(string term, double score)>();
                    foreach (var kvp in termFreq)
                    {
                        var tf = (double)kvp.Value / maxFreq;
                        var tfidf = tf * idf[kvp.Key];
                        tfidfScores.Add((kvp.Key, tfidf));
                    }

                    result[docIdx] = tfidfScores
                        .OrderByDescending(x => x.score)
                        .Take(topN)
                        .ToList();
                }

                return result;
            }
            catch
            {
                // Fallback to simple keyword extraction
                var result = new Dictionary<int, List<(string, double)>>();
                for (int i = 0; i < texts.Count; i++)
                {
                    result[i] = ExtractKeywords(texts[i], topN);
                }
                return result;
            }
        }

        public Dictionary<string, List<string>> ExtractEntities(string text)
        {
            var entities = new Dictionary<string, List<string>>
            {
                ["concepts"] = new List<string>(),
                ["actions"] = new List<string>(),
                ["attributes"] = new List<string>()
            };

            // Extract capitalized words as potential entities
            var capitalized = Regex.Matches(text, @"[А-ЯЁA-Z][а-яёa-z]+");
            entities["concepts"].AddRange(capitalized.Cast<Match>().Select(m => m.Value));

            // Extract words that appear after common action indicators
            var actionIndicators = new[] { "создать", "построить", "сделать", "выстраивать", "воспроизвести",
                                          "create", "build", "make", "construct", "reproduce" };

            var words = text.ToLower().Split();
            for (int i = 0; i < words.Length; i++)
            {
                if (actionIndicators.Any(indicator => words[i].Contains(indicator)))
                {
                    if (i + 1 < words.Length)
                    {
                        entities["actions"].Add(words[i + 1]);
                    }
                }
            }

            // Extract adjectives and attributes (simple heuristic)
            var adjectivePatterns = new[] { @"\w+ный", @"\w+кий", @"\w+ской", @"\w+ive", @"\w+al", @"\w+ful" };
            foreach (var pattern in adjectivePatterns)
            {
                var matches = Regex.Matches(text.ToLower(), pattern);
                entities["attributes"].AddRange(matches.Cast<Match>().Select(m => m.Value));
            }

            return entities;
        }

        public List<Dictionary<string, string>> DetectRelationships(string text)
        {
            var relationships = new List<Dictionary<string, string>>();

            // Common relationship patterns
            var patterns = new[]
            {
                (@"(\w+)\s+(?:является|есть|это)\s+(\w+)", "is_a"),
                (@"(\w+)\s+(?:содержит|включает|имеет)\s+(\w+)", "has"),
                (@"(\w+)\s+(?:создает|генерирует|производит)\s+(\w+)", "creates"),
                (@"(\w+)\s+(?:связан|связана|связано)\s+(?:с|со)\s+(\w+)", "related_to"),
                (@"(\w+)\s+(?:через|посредством|с помощью)\s+(\w+)", "via")
            };

            foreach (var (pattern, relType) in patterns)
            {
                var matches = Regex.Matches(text.ToLower(), pattern);
                foreach (Match match in matches)
                {
                    relationships.Add(new Dictionary<string, string>
                    {
                        ["from"] = match.Groups[1].Value,
                        ["to"] = match.Groups[2].Value,
                        ["type"] = relType
                    });
                }
            }

            return relationships;
        }

        public double CalculateConceptSimilarity(List<string> concepts1, List<string> concepts2)
        {
            var set1 = new HashSet<string>(concepts1);
            var set2 = new HashSet<string>(concepts2);

            if (set1.Count == 0 || set2.Count == 0)
                return 0.0;

            var intersection = set1.Intersect(set2).Count();
            var union = set1.Union(set2).Count();

            return union > 0 ? (double)intersection / union : 0.0;
        }

        public ConceptGraph BuildConceptGraph(string text)
        {
            var keywords = ExtractKeywords(text, 15);
            var entities = ExtractEntities(text);
            var relationships = DetectRelationships(text);

            var graph = new ConceptGraph
            {
                Nodes = new List<ConceptNode>(),
                Edges = new List<ConceptEdge>()
            };

            // Add keyword nodes
            foreach (var (keyword, score) in keywords)
            {
                graph.Nodes.Add(new ConceptNode
                {
                    Id = keyword,
                    Type = "keyword",
                    Weight = score
                });
            }

            // Add entity nodes
            foreach (var entityType in entities.Keys)
            {
                foreach (var entity in entities[entityType].Take(5))
                {
                    if (!graph.Nodes.Any(n => n.Id == entity.ToLower()))
                    {
                        graph.Nodes.Add(new ConceptNode
                        {
                            Id = entity.ToLower(),
                            Type = entityType,
                            Weight = 0.5
                        });
                    }
                }
            }

            // Add relationship edges
            foreach (var rel in relationships)
            {
                graph.Edges.Add(new ConceptEdge
                {
                    From = rel["from"],
                    To = rel["to"],
                    Type = rel["type"],
                    Weight = 1.0
                });
            }

            // Add co-occurrence edges
            var words = PreprocessText(text);
            var keywordIds = keywords.Select(k => k.Keyword).ToList();

            for (int i = 0; i < keywordIds.Count; i++)
            {
                var kw1 = keywordIds[i];
                for (int j = i + 1; j < keywordIds.Count; j++)
                {
                    var kw2 = keywordIds[j];

                    if (words.Contains(kw1) && words.Contains(kw2))
                    {
                        // Calculate co-occurrence score
                        var kw1Positions = words.Select((w, idx) => new { w, idx })
                            .Where(x => x.w == kw1).Select(x => x.idx).ToList();
                        var kw2Positions = words.Select((w, idx) => new { w, idx })
                            .Where(x => x.w == kw2).Select(x => x.idx).ToList();

                        if (kw1Positions.Any() && kw2Positions.Any())
                        {
                            var minDistance = kw1Positions.SelectMany(p1 =>
                                kw2Positions.Select(p2 => Math.Abs(p1 - p2))).Min();

                            if (minDistance < 10)
                            {
                                var weight = 1.0 / (minDistance + 1);
                                graph.Edges.Add(new ConceptEdge
                                {
                                    From = kw1,
                                    To = kw2,
                                    Type = "co_occurrence",
                                    Weight = weight
                                });
                            }
                        }
                    }
                }
            }

            return graph;
        }
    }

    public class ConceptGraph
    {
        public List<ConceptNode> Nodes { get; set; } = new List<ConceptNode>();
        public List<ConceptEdge> Edges { get; set; } = new List<ConceptEdge>();
    }

    public class ConceptNode
    {
        public string Id { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public double Weight { get; set; }
    }

    public class ConceptEdge
    {
        public string From { get; set; } = string.Empty;
        public string To { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public double Weight { get; set; }
    }
}
