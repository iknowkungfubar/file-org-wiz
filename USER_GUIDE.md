# file-org-wiz Comprehensive User Guide

> Everything you need to know about using file-org-wiz for complete file organization.

---

## Table of Contents

1. [Understanding Para](#1-understanding-para)
2. [The File System](#2-the-file-system)
3. [Naming Conventions](#3-naming-conventions)
4. [Daily Workflow](#4-daily-workflow)
5. [Periodic Maintenance](#5-periodic-maintenance)
6. [Advanced Topics](#6-advanced-topics)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Understanding PARA

### What is PARA?

PARA is a file organization methodology created by productivity expert Tiago Forte. It organizes by *action*, not *topic*.

| Category | What Goes Here | Example |
|----------|----------------|---------|
| **Projects** | Time-bound work with deadline | Job search, client project, course creation |
| **Areas** | Ongoing responsibilities | Health, finances, home maintenance |
| **Resources** | Reference material | AI research, code snippets, recipes |
| **Archive** | Completed/obsolete items | Old projects, outdated docs |

### Why PARA Works

- **Action-oriented**: Matches how you actually live
- **Four categories max**: Easy to decide where things go
- **Evolves with life**: Projects become areas become archives naturally

### The Zettelkasten Connection

For note-taking and knowledge, Zettelkasten adds:
- **Atomic notes**: One idea per note
- **Bidirectional links**: Notes connect to each other
- **Maps of Content**: Topic indexes

Together: PARA organizes files, Zettelkasten organizes knowledge.

---

## 2. The File System

### Folder Structure

```
MOUNT_PATH/
├── 00_INBOX/                    # ⭐ DAILY: Drop zone
├── 01_PROJECTS/               # Time-bound work
│   ├── Projects/
│   ├── Client-Work/
│   └── [your projects]/
├── 02_AREAS/                  # Ongoing responsibilities
│   ├── Health/
│   ├── Finance/
│   ├── Home/
│   ├── Learning/
│   └── Personal/
├── 03_RESOURCES/              # Reference material
│   ├── AI/
│   ├── Tech/
│   ├── Career/
│   ├── Development/
│   ├── Media/
│   ├── Reading/
│   ├── Tools/
│   └── Distributions/
├── 04_ARCHIVE/               # Completed items
├── 90_TEMPLATES/             # Reusable templates
└── 99_SYSTEM/                # Rules & docs
    ├── File Naming Rules.md
    ├── Tag Rules.md
    ├── Vault Rules.md
    └── File_System_User_Guide.md
```

### Where Files Belong

| File Type | Go To | Example |
|----------|-------|---------|
| Active business docs | `01_PROJECTS/YourProject/` | Proposal, contract |
| Job search materials | `01_PROJECTS/Career-Search/` | Resume, applications |
| Health records | `02_AREAS/Health/` | Medical, prescriptions |
| Financial docs | `02_AREAS/Finance/` | Tax, investments |
| Code snippets | `03_RESOURCES/Development/` | Scripts, configs |
| AI research | `03_RESOURCES/AI/` | Prompt library |
| Old projects | `04_ARCHIVE/` | Completed work |
| Templates | `90_TEMPLATES/` | Meeting, invoice |

---

## 3. Naming Conventions

### The Pattern

```
YYYY-MM-DD__context__description__vNN.ext
```

### Breaking It Down

| Part | Meaning | Example |
|------|---------|---------|
| `YYYY-MM-DD` | Date (ISO) | 2026-04-25 |
| `__context` | Project/area slug | `__career`, `__turin-tech` |
| `__description` | What it is | `__resume`, `__pitch-deck` |
| `__vNN` | Version | `__v01`, `__v02` |
| `.ext` | Extension | `.pdf`, `.docx` |

### Examples

| Document | Correct Name |
|----------|-------------|
| Resume dated April 24, 2026 | `2026-04-24__career__resume__v01.docx` |
| Pitch deck, v2 | `2026-04-20__turin-tech__pitch-deck__v02.pdf` |
| Meeting notes | `2026-04-25__project__weekly-sync__v01.md` |

### Context Slugs

Create slugs for your projects/areas:

| Project/Area | Slug |
|-------------|-----|
| Your business | `turin-tech` |
| Job search | `career` |
| Health | `health` |
| Home | `home` |
| Game project | `game-symbiosis` |

### Anti-Patterns (Don't Do This)

| Bad Name | Why |
|---------|-----|
| `final.docx` | Which final? |
| `final2.docx` | What changed? |
| `my doc.docx` | Ambiguous |
| `Meeting Notes 4-24.docx` | No sorting |
| `RESUME FINAL v3 EDITED.docx` | Version soup |

---

## 4. Daily Workflow

### Morning (5 minutes)

1. **Open the system**: Navigate to your mount point
2. **Check 00_INBOX**: Any files to process?
3. **Review 00_INBOX**: Move to proper folder or delete

### During the Day

#### New File Workflow

1. Save new file to `00_INBOX` temporarily
2. Determine category:
   - Time-bound? → `01_PROJECTS/`
   - Ongoing area? → `02_AREAS/`
   - Reference? → `03_RESOURCES/`
   - Done? → `04_ARCHIVE/`
3. Apply naming convention
4. Move to correct folder

#### Finding Files

1. **Search by name**: Use OS search
2. **Search by pattern**: `YYYY-MM-DD__*`
3. **Navigate by folder**: Use structure above
4. **Check tags**: Use tag-based search

### Evening (5 minutes)

1. **Process 00_INBOX**: Clear any remaining items
2. **Review day**: What did you create?
3. **Tomorrow**: Set priorities for tomorrow

---

## 5. Periodic Maintenance

### Weekly (30 minutes)

- [ ] Review 00_INBOX (should be empty)
- [ ] Review 04_ARCHIVE (any to delete?)
- [ ] Update MOC files
- [ ] Check naming consistency
- [ ] Backup verified working

### Monthly (60 minutes)

- [ ] Review all projects (move completed to archive)
- [ ] Update folder structure if needed
- [ ] Clean up duplicate files
- [ ] Test backup restoration
- [ ] Review naming conventions

### Quarterly (half day)

- [ ] Full system review
- [ ] Archive old items (12+ months)
- [ ] Update context slugs
- [ ] Review and update guides
- [ ] Plan next quarter

---

## 6. Advanced Topics

### Using with Obsidian Vault

Your vault at `YOUR_VAULT/` should mirror:

```
YOUR_VAULT/
├── 00_HOME/           # Entry points
├── 01_PROJECTS/       # Project notes
├── 02_AREAS/         # Area dashboards
├── 03_RESOURCES/     # Reference notes
├── 04_LOGS/          # Daily/Weekly
├── 90_TEMPLATES/    # Templates
└── 99_SYSTEM/       # Rules
```

### Tags

Use nested tags for flexibility:

```
#type/meeting
#status/active  
#project/turin-tech
#topic/ai
```

### Using the MCP Server

Start server:

```bash
python mcp_server.py --port 5000 \
  --mount /your/mount \
  --backup /your/backup
```

API calls:

```bash
# Organize
curl -X POST localhost:5000/organize \
  -d '{"mount_path": "/mount", "backup_path": "/backup"}'

# Get structure
curl localhost:5000/structure?path=/mount
```

---

## 7. Troubleshooting

### "Where did I put X?"

1. Use OS search with date pattern: `2026-04-*__*resume*`
2. Check each top-level folder
3. Check 00_INBOX (temporary home)
4. Use `structure` API endpoint

### "What's a context slug?"

Used in naming: `2026-04-25__SLUG__description`

Create slugs for your main areas:
- Projects: `project-name`
- Areas: area name (health, career, home)

### "System feels broken"

1. Check `99_SYSTEM/File_System_User_Guide.md` exists
2. Verify backup exists
3. Check naming rules applied
4. Re-read this guide

### "Files not appearing"

1. Check server running: `curl localhost:5000/health`
2. Check folder exists: `ls /mount/00_INBOX/`
3. Try refresh: restart server

### Backups

Backups are timestamped:
```
/your/backup/backup__2026-04-25_15-30-00/
```

Restore by copying back:
```bash
cp -r /backup/backup__2026-04-25_*/* /mount/
```

---

## Quick Reference Card

### Quick Decision Tree

```
Is it time-bound? → 01_PROJECTS/
Is it ongoing? → 02_AREAS/
Is it reference? → 03_RESOURCES/
Is it done? → 04_ARCHIVE/
```

### Naming Cheatsheet

```
Pattern: YYYY-MM-DD__context__description__vNN.ext
Date first, context slug, lowercase description, version
NO SPACES - use hyphens
NO SPECIAL CHARACTERS
```

### Finding Files

| Method | Use |
|--------|-----|
| OS Search | By filename |
| Structure | By folder |
| Tags | By metadata |
| API | Programmatic |

---

## Learn More

- Quick Start: [QUICKSTART.md](./QUICKSTART.md)
- FAQ: [FAQ.md](./FAQ.md)
- Methodology: [Why_PARA_Zettelkasten.md](./Why_PARA_Zettelkasten.md)
- Full Prompt: [AI_File_Organization_Agent_Prompt.md](./AI_File_Organization_Agent_Prompt.md)

---

*Last updated: 2026-04-25*
*Version: 1.0.0*