import ast
import hashlib
import os
import sqlite3

MEMORY_DB = os.path.expanduser("~/genetic_flow/tracking_db/memory.db")

class SymbolicParser:
    """[PERFORMATIVE: TOKENIZE] Compiles live files into structured AST nodes."""

    def __init__(self, db_path=MEMORY_DB):
        self.db_path = db_path

    def get_signature_hash(self, code):
        """Generates context signature hashes via MD5 token strings."""
        try:
            tree = ast.parse(code)
            # Generate a structural representation of the AST
            struct_repr = self._get_structural_string(tree)
            sig_hash = hashlib.md5(struct_repr.encode()).hexdigest()
            return sig_hash, struct_repr
        except Exception as e:
            return None, str(e)

    def _get_structural_string(self, node):
        """Recursive AST walker to build a structural signature string."""
        node_type = type(node).__name__
        children = []
        for child in ast.iter_child_nodes(node):
            children.append(self._get_structural_string(child))

        if not children:
            return node_type
        return f"{node_type}({','.join(children)})"

    def map_token_relations(self, code):
        """Extracts parent/child node shapes for the relational matrix."""
        try:
            tree = ast.parse(code)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for node in ast.walk(tree):
                parent_type = type(node).__name__
                for child in ast.iter_child_nodes(node):
                    child_type = type(child).__name__
                    cursor.execute("""
                        INSERT INTO token_relational_matrix (parent_node, child_node)
                        VALUES (?, ?)
                        ON CONFLICT(parent_node, child_node) DO UPDATE SET
                        occurrence_count = occurrence_count + 1
                    """, (parent_type, child_type))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Parser Error: {e}")
            return False

if __name__ == "__main__":
    parser = SymbolicParser()
    test_code = "def algorithm(n): return n & 1"
    h, s = parser.get_signature_hash(test_code)
    print(f"Hash: {h}\nStructure: {s}")
