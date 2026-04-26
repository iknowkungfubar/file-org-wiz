# file-org-wiz Reference Card

> Print and keep handy.

---

## PARA Folders

| Folder | What Goes Here | Example |
|--------|----------------|---------|
| `00_INBOX/` | Drop zone, process daily | New downloads |
| `01_PROJECTS/` | Active time-bound work | Client projects |
| `02_AREAS/` | Ongoing responsibilities | Health, Finance |
| `03_RESOURCES/` | Reference material | Code, AI, Reading |
| `04_ARCHIVE/` | Completed items | Old projects |
| `90_TEMPLATES/` | Reusable templates | Meeting template |
| `99_SYSTEM/` | Rules & docs | This card |

---

## File Naming

```
YYYY-MM-DD__context__description__vNN.ext
```

| Part | Meaning |
|------|----------|
| `YYYY-MM-DD` | Date |
| `__context` | Project/area slug |
| `__description` | What it is |
| `__vNN` | Version |

**Examples:**
- `2026-04-25__career__resume__v01.docx`
- `2026-04-24__turin-tech__pitch-deck__v02.pdf`

---

## Decision Tree

```
Is it time-bound? → 01_PROJECTS/
Is it ongoing? → 02_AREAS/
Is it reference? → 03_RESOURCES/
Is it done? → 04_ARCHIVE/
```

---

## API Commands

```bash
# Organize
curl -X POST localhost:5000/organize -d '{"mount_path": "/mount"}'

# Get structure  
curl localhost:5000/structure?path=/mount

# Check health
curl localhost:5000/health

# Apply naming
curl -X POST localhost:5000/apply-names -d '{
  "file_path": "/file.pdf",
  "context": "project",
  "description": "doc",
  "version": 1
}'
```

---

## Port Reference

| Port | System |
|------|--------|
| 5000 | Default |
| 5001 | Claude Desktop |
| 5002 | Cursor |
| 5003 | Codex |
| 5004 | Cody |

---

## Daily Routine

| When | Action | Time |
|------|--------|------|
| Morning | Check 00_INBOX | 2 min |
| During | Organize new files | 1 min |
| Evening | Clear 00_INBOX | 2 min |
| Weekly | Full review | 30 min |

---

## Key Files

| File | Purpose |
|------|---------|
| `99_SYSTEM/File Naming Rules.md` | Naming guide |
| `99_SYSTEM/Tag Rules.md` | Tag system |
| `99_SYSTEM/Vault Rules.md` | Obsidian setup |
| `99_SYSTEM/File_System_User_Guide.md` | Full guide |

---

## Don't

- ❌ Spaces in filenames
- ❌ Special chars: `: * ? " < > | / \`
- ❌ `final`, `final2`, `finalFINAL`
- ❌ Dates not first: `Meeting 4-25.docx`

---

## Do

- ✅ Hyphens or underscores
- ✅ Date first: `2026-04-25`  
- ✅ Context slug: `__career__`, `__turin-tech__`
- ✅ Version: `__v01`

---

*file-org-wiz v1.3.0*
*Keep this card visible!*