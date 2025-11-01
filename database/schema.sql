-- Metatron AGI Database Schema
-- Based on ERM Model for multidimensional knowledge representation
-- This schema supports heuristic-based concept extraction and world building

-- Resource table for tracking available computational resources
CREATE TABLE IF NOT EXISTS Resource (
    Id SERIAL PRIMARY KEY,
    LLMProvider INT, -- [1 - OpenAI, 2 - Gemini, 3 - DeepSeek, 4 - Grok] (optional for future use)
    QuantumProvider INT, -- [1 - Google, ...] (optional for future use)
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quantum Computer resources
CREATE TABLE IF NOT EXISTS QuantumComputer (
    Id BIGSERIAL PRIMARY KEY,
    ResourceId INT REFERENCES Resource(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LLM Agent resources (for future extensibility)
CREATE TABLE IF NOT EXISTS LLMAgent (
    Id BIGSERIAL PRIMARY KEY,
    ResourceId INT REFERENCES Resource(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Space: Represents different conceptual, visual, or temporal spaces
CREATE TABLE IF NOT EXISTS Space (
    Id BIGSERIAL PRIMARY KEY,
    Type INT NOT NULL, -- [1 - Conceptual, 2 - Visual, 3 - Temporal]
    Name VARCHAR(250),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Singularity: Core semantic graph nodes that define tasks and contain knowledge
CREATE TABLE IF NOT EXISTS Singularity (
    Id BIGSERIAL PRIMARY KEY,
    Task TEXT,
    TaskLLMVector JSONB, -- For future LLM integration (currently using heuristic vectors)
    LayersCount INT DEFAULT 0,
    VisualRepresentation JSONB,
    Content TEXT,
    Version INT DEFAULT 1,
    SpaceId BIGINT REFERENCES Space(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Object: Entities in the knowledge space
CREATE TABLE IF NOT EXISTS Object (
    Id BIGSERIAL PRIMARY KEY,
    IsSubject BOOLEAN DEFAULT FALSE,
    Name VARCHAR(250),
    Type VARCHAR(10),
    Data JSONB,
    SingularityId BIGINT REFERENCES Singularity(Id),
    SpaceId BIGINT REFERENCES Space(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector: Embeddings and vector representations
CREATE TABLE IF NOT EXISTS Vector (
    Id BIGSERIAL PRIMARY KEY,
    Data JSONB NOT NULL,
    ExternalId BIGINT,
    Content TEXT,
    SingularityId BIGINT REFERENCES Singularity(Id),
    SpaceId BIGINT REFERENCES Space(Id),
    ObjectId BIGINT REFERENCES Object(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Point: Individual knowledge points or agents within a singularity
CREATE TABLE IF NOT EXISTS Point (
    Id BIGSERIAL PRIMARY KEY,
    Task TEXT,
    TaskLLMVector JSONB,
    TaskContextLLMVector JSONB,
    IsSuperCluster BOOLEAN DEFAULT FALSE,
    PositionVector JSONB,
    Layer INT DEFAULT 0,
    QuantumTask JSONB,
    QuantumSpace JSONB,
    VisualRepresentation JSONB,
    SpaceDimension INT,
    Name VARCHAR(250),
    Content TEXT,
    Weight FLOAT DEFAULT 1.0,
    Type INT, -- [1 - resource, 2 - content, 3 - semantic]
    SingularityId BIGINT REFERENCES Singularity(Id),
    VectorId BIGINT REFERENCES Vector(Id),
    ObjectId BIGINT REFERENCES Object(Id),
    ComputerId BIGINT REFERENCES QuantumComputer(Id),
    AgentId BIGINT REFERENCES LLMAgent(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update Vector table to add Point reference
ALTER TABLE Vector ADD COLUMN IF NOT EXISTS PointId BIGINT REFERENCES Point(Id);

-- PointTimeSpace: Temporal snapshots of points
CREATE TABLE IF NOT EXISTS PointTimeSpace (
    Id BIGSERIAL PRIMARY KEY,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Snapshot JSONB,
    PointId BIGINT REFERENCES Point(Id) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relation: Relationships between objects in space
CREATE TABLE IF NOT EXISTS Relation (
    Id BIGSERIAL PRIMARY KEY,
    Type VARCHAR(50) NOT NULL,
    SingularityId BIGINT REFERENCES Singularity(Id),
    FromObjectId BIGINT REFERENCES Object(Id),
    ToObjectId BIGINT REFERENCES Object(Id),
    SpaceId BIGINT REFERENCES Space(Id),
    Weight FLOAT DEFAULT 1.0,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Segment: Knowledge segments connecting two points
CREATE TABLE IF NOT EXISTS Segment (
    Id BIGSERIAL PRIMARY KEY,
    TypeName VARCHAR(50),
    Type INT,
    Weight FLOAT DEFAULT 1.0,
    SingularityId BIGINT REFERENCES Singularity(Id),
    FromPointId BIGINT REFERENCES Point(Id),
    ToPointId BIGINT REFERENCES Point(Id),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_singularity_space ON Singularity(SpaceId);
CREATE INDEX IF NOT EXISTS idx_point_singularity ON Point(SingularityId);
CREATE INDEX IF NOT EXISTS idx_point_type ON Point(Type);
CREATE INDEX IF NOT EXISTS idx_segment_singularity ON Segment(SingularityId);
CREATE INDEX IF NOT EXISTS idx_segment_points ON Segment(FromPointId, ToPointId);
CREATE INDEX IF NOT EXISTS idx_relation_space ON Relation(SpaceId);
CREATE INDEX IF NOT EXISTS idx_relation_objects ON Relation(FromObjectId, ToObjectId);
CREATE INDEX IF NOT EXISTS idx_object_space ON Object(SpaceId);
CREATE INDEX IF NOT EXISTS idx_vector_point ON Vector(PointId);
CREATE INDEX IF NOT EXISTS idx_pointtimespace_point ON PointTimeSpace(PointId);
CREATE INDEX IF NOT EXISTS idx_pointtimespace_time ON PointTimeSpace(Time);

-- Create function to update UpdatedAt timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.UpdatedAt = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_singularity_updated_at BEFORE UPDATE ON Singularity
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_point_updated_at BEFORE UPDATE ON Point
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_space_updated_at BEFORE UPDATE ON Space
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_object_updated_at BEFORE UPDATE ON Object
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_relation_updated_at BEFORE UPDATE ON Relation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_segment_updated_at BEFORE UPDATE ON Segment
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
