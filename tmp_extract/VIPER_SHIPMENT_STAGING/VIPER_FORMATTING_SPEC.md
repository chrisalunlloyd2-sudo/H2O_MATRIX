# 📐 VIPER NOTES: FORMATTING & ARCHITECTURAL SPECIFICATION
*Version 1.0 - Derived from VIPER_GLOBAL_VIEW Success*

## 1. Core Structural Pattern
All `viper notes` must follow the **Multi-Tree Heuristic** hierarchy for compatibility with the Global Matrix.

### **Pathing Convention**
`[SUBDOMAIN] ➔ [LOGIC_BLOCK] ➔ [ENTITY] ➔ {FILENAME}`

### **Primary Subdomains**
- **SOPs:** Foundational Operating Procedures and Laws.
- **Logic:** Core algorithmic flows and reasoning branches.
- **Viper Journal:** Daily execution logs and personal captures.
- **Viper Notes:** Research, facts, and static documentation.
- **Projects:** Grouped by `[PROJECT_ID]`.

## 2. File Metadata Requirements
To ensure the Stochastic Matrix can parse the data, every `.md` or `.txt` file should include:
- **Timestamp:** Creation and last mutation.
- **Source:** The context window or system that produced the entry.
- **Fencing:** Use `BLOCKS_OF_TEXT` formatting for large entries.

## 3. The 4-Link Interaction Flow
`LAPTOP_HD` nodes must implement the following UI/UX flow for parity:
1. **Agent Select:** Individualized chat sessions per swarm node.
2. **Interactive Fallback:** Intelligent conversational responses when the primary mesh is unreachable.
3. **Topological Search:** Default to tree-view, fallback to keyword matrix search.
4. **Note Reader:** Monospaced rendering with system-level **COPY** (Clipboard) capability for context extraction.

## 4. Theme Parity
- **Dark Mode:** `#0A0A0A` background / `#00FF00` primary text.
- **Light Mode:** `#F0F0F0` background / `#007700` primary text.
- **Zero-Restart Swapping:** Themes must be applied live to all UI adapters.
