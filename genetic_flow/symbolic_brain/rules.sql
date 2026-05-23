-- Master Schema for Symbolic Brain
-- Mapping logic constraints and rule weights

-- 1. Structural Token Dictionary (Vocab equivalent)
CREATE TABLE IF NOT EXISTS token_relational_matrix (
    parent_node TEXT,
    child_node TEXT,
    occurrence_count INTEGER DEFAULT 1,
    PRIMARY KEY (parent_node, child_node)
);

-- 2. Context Signature Hashes (Embedding equivalent)
CREATE TABLE IF NOT EXISTS context_signatures (
    signature_hash TEXT PRIMARY KEY, -- MD5 of AST structural string
    raw_structure TEXT,
    last_seen_gen INTEGER
);

-- 3. Production Optimization Rules (Projection Weights equivalent)
CREATE TABLE IF NOT EXISTS production_rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_signature TEXT,
    transformation_directive TEXT,
    current_rule_weight REAL DEFAULT 1.0, -- Logarithmic scalar
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    FOREIGN KEY (target_signature) REFERENCES context_signatures(signature_hash)
);

-- Seed initial optimization directives
INSERT OR IGNORE INTO production_rules (target_signature, transformation_directive, current_rule_weight)
VALUES 
('global', 'Minimize global scope lookups; cache variables locally.', 1.2),
('loop', 'Unroll range-based loops with small constant bounds.', 1.5),
('math', 'Replace standard math calls with bitwise equivalents where applicable.', 1.4);

-- Cluster Weight Bias: {"fn": 1.5, "pub": 1.2, "impl": 1.4}

-- Cluster Weight Bias: {"fn": 1.5, "pub": 1.2, "impl": 1.4}
