# file-org-wiz Roadmap

> Future improvements and fixes for the File Organization Wizard MCP Server.

---

## Status: COMPLETED (v1.1.0)

All roadmap items have been implemented:

| Priority | Feature | Status |
|----------|---------|--------|
| 0 | Deep file scanning | ✅ Implemented |
| 0 | Duplicate detection | ✅ Implemented |
| 1 | Enhanced organize endpoint | ✅ Implemented |
| 1 | MOC Generator | ✅ Implemented |
| 1 | Atomic Note Creator | ✅ Implemented |
| 1 | Link Scanner | ✅ Implemented |
| 2 | Dry-Run Mode | ✅ Implemented |
| 2 | Tests | ✅ 83 tests passing |

---

## Executive Summary

Based on user feedback and research into PARA + Zettelkasten methodologies, this roadmap addresses core issues:

1. **Shallow organization** - Current implementation doesn't deeply scan/analyze files
2. **Missing duplicate handling** - No detection or merge capability
3. **Incomplete PARA logic** - Categorization is too simplistic
4. **No Zettelkasten features** - Missing MOCs, atomic notes, bidirectional linking

---

## Priority 0: Critical Fixes (Immediate)

### Issue 0.1: Deep File Scanning ✅ COMPLETED
**Problem:** The organize function only creates folder structure but doesn't actually categorize or move existing files.

**Root Cause:** `create_folder_structure()` only makes directories, doesn't process files.

**Solution:** Add deep file scanning + intelligent categorization phase. (IMPLEMENTED)

### Issue 0.2: Duplicate Detection
**Problem:** User reports duplicates not handled, files missed.

**Root Cause:** No duplicate detection algorithm implemented.

**Solution:** Implement content-based + filename-based duplicate detection.

---

## Priority 1: Core Functionality (High)

### Feature 1.1: Deep File Scanner
**Description:** Recursively scan all files, analyze their content/metadata for intelligent categorization.

```
scan_and_analyze(base_path)
├── Collect all files recursively
├── Extract metadata (type, date, size, content)
├── Classify by content type
└── Suggest PARA category
```

| File Type | Suggested Category |
|----------|------------------|
| .psd, .ai, .sketch | 01_PROJECTS/Projects |
| .pdf (invoice, contract) | 02_AREAS/Finance |
| .md notes | 03_RESOURCES/... |
| Completed project files | 04_ARCHIVE |

**Research Sources:**
- [Tiago Forte's PARA method](https://blog.make10000hour.com/post/para-method)
- [10kHours PARA Guide](https://productivitystack.io/guides/building-a-second-brain/)

### Feature 1.2: Duplicate Detection & Merge
**Description:** Find duplicates by content hash + filename similarity, merge keeping newer.

**Algorithm:**
1. Group by file size (fast filter)
2. Quick hash (first/last 4KB) for candidates
3. Full SHA256 for verification
4. Filename similarity (fuzzy matching)
5. Merge keeping newer (by mtime)

**Research Sources:**
- [pydupes](https://github.com/erikreed/pydupes) - Parallel duplicate finder
- [barrust/dup-file-finder](https://github.com/barrust/dup-file-finder) - SQLite-backed
- [fdupes](https://github.com/adrianlopezroche/fdupes) - Solid reference

**Merge Strategy:**
```
Duplicate Set: [file_v1.txt, file_v2.txt, document-FINAL.txt]
                ↓
               mtime comparison
                ↓
Keep: document-FINAL.txt (newest)
Archive: others → 04_ARCHIVE/.duplicates/
```

### Feature 1.3: Enhanced PARA Categorization
**Description:** Improve categorization logic beyond folder creation.

**Improvements:**
- Content-based classification (invoice → Finance, resume → Career)
- Pattern-based rules (YYYY-MM-DD in name → keep naming convention)
- Date-based sorting (recent → Projects/Personal, old → Archive)
- Custom rules file support

**Categorization Logic:**
```python
def categorize_file(path: str, rules: dict) -> str:
    """
    Return suggested PARA folder based on:
    1. File extension/content type
    2. Filename patterns
    3. Modification date
    4. Custom rules
    """
    # Implementation details in SPEC.md
```

---

## Priority 2: Zettelkasten Integration (Medium)

### Feature 2.1: MOC Generator
**Description:** Auto-generate Maps of Content for Obsidian vaults.

**Research Sources:**
- [Zoottelkeeper](https://obsidianstats.com/plugins/zoottelkeeper-obsidian-plugin)
- [LYT - Linking Your Thinking](https://publish.obsidian.md/hub/04+-+Areas+of+Knowledge/Linking+Your+Thinking+Home)

**Implementation:**
```
For each topic folder with 5+ notes:
    Generate: TOPIC MOC.md
    ├── List all notes in folder
    ├── Add [[wikilink]] references
    └── Add tag frontmatter
```

### Feature 2.2: Atomic Note Creator
**Description:** Convert long notes into atomic (one idea each) notes.

**Rules:**
- One heading = one note
- Split on ## or ### headings
- Add unique ID (YYYYMMDDHHMMSS)
- Preserve links

### Feature 2.3: Bidirectional Link Scanner
**Description:** Analyze notes and suggest missing links.

**Algorithm:**
1. Extract all [[wikilinks]] from vault
2. Build link graph
3. Find semantically similar content
4. Suggest links (optional, with confidence score)

---

## Priority 3: UX Improvements (Lower)

### Feature 3.1: Dry-Run Mode
**Description:** Preview changes before applying.

**API Addition:**
```json
POST /organize
{
  "mount_path": "/path",
  "dry_run": true
}
```

**Response:**
```json
{
  "suggested_actions": [
    {"action": "move", "from": "x", "to": "y", "reason": "Categorization"},
    {"action": "merge", "duplicates": ["a", "b"], "keep": "a"}
  ]
}
```

### Feature 3.2: Progress WebSocket
**Description:** Real-time progress for long operations.

### Feature 3.3: Interactive CLI
**Description:** TUI for file-by-file decisions.

---

## Technical Architecture

### New Module Structure

```
src/
├── mcp_server.py          # Flask server (existing)
├── scanner/
│   ├── __init__.py
│   ├── deep_scan.py      # Recursive file analysis
│   └── classifier.py   # PARA categorization logic
├── duplicates/
│   ├── __init__.py
│   ├── detector.py     # Hash-based detection
│   └── merger.py      # Merge strategy
└── zettelkasten/
    ├── __init__.py
    ├── moc.py         # MOC generator
    └── linker.py     # Link suggestions
```

### Priority Order for Implementation

| Priority | Feature | Files to Modify |
|----------|---------|---------------|
| 0 | Deep scan + categorize | scanner/deep_scan.py, classifier.py |
| 0 | Duplicate detection | duplicates/detector.py, merger.py |
| 1 | Enhanced organize endpoint | mcp_server.py |
| 1 | Tests | tests/test_scanner.py, test_duplicates.py |
| 2 | MOC generator | zettelkasten/moc.py |
| 2 | Link suggestions | zettelkasten/linker.py |
| 3 | Dry-run mode | mcp_server.py |

---

## Backward Compatibility

**Breaking Changes to Avoid:**
- Keep existing `/organize` schema compatible
- Add new optional params (not required)
- Deprecate slowly with warnings

---

## Testing Strategy

### Test Coverage Targets

| Module | Current | Target |
|--------|---------|--------|
| security | 100% | 100% |
| core functions | 80% | 90% |
| scanner | 0% | 85% |
| duplicates | 0% | 90% |
| zettelkasten | 0% | 80% |

---

## Open Questions

1. **Content analysis depth?** - Full file reading vs. metadata only
2. **Merge strategy?** - Always auto-merge or prompt user?
3. **Zettelkasten optional?** - Feature flag for vault creation
4. **Performance expectations?** - File count limits

---

## References

### PARA Implementation
- [Tiago Forte - PARA](https://forte.la/paraguide)
- [PARA in Practice](https://blog.make10000hour.com/post/para-method)

### Zettelkasten
- [Obsidian MOCs](https://publish.obsidian.md/hub/04+-+Areas+of+Knowledge/Linking+Your+Thinking+Home)
- [AI + Zettelkasten](https://www.codewithseb.com/blog/ai-zettelkasten-obsidian-claude-knowledge-graph)

### Duplicate Detection
- [fdupes](https://github.com/adrianlopezroche/fdupes)
- [pydupes](https://github.com/erikreed/pydupes)

---

*Last Updated: 2026-04-25*
*Status: COMPLETED (v1.1.0)*