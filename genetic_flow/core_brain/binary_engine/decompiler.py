import dis
import math
import collections

class BinaryDecompilationEngine:
    """Airgapped processor that translates Python logic into binary opcode math."""

    def decompile_and_score(self, executable_code_str: str) -> float:
        """Returns the Shannon Entropy H(B) of the compiled binary footprint."""
        try:
            # 1. Compile to raw binary bytecode space
            compiled_bytecode = compile(executable_code_str, '<string>', 'exec')

            # 2. Extract opcode integers (Bytecode instructions)
            opcodes = []
            for instr in dis.get_instructions(compiled_bytecode):
                opcodes.append(instr.opcode)

            if not opcodes:
                return 0.0

            # 3. Calculate Shannon Entropy H = -sum(p_i * log2(p_i))
            counts = collections.Counter(opcodes)
            total = len(opcodes)
            entropy = 0.0
            for count in counts.values():
                p = count / total
                entropy -= p * math.log2(p)

            return entropy

        except Exception as e:
            print(f" [!] Binary Decompilation Error: {e}")
            return 999.0 # High penalty for non-compilable code
