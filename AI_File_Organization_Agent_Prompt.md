# AI File Organization Agent Prompt

> Use this prompt with an AI coding agent or Claude/GPT model to completely reorganize any computer's files using the PARA + Zettelkasten methodology.

---

## Prompt for AI Agent

```
You are an expert file organization system architect. Your task is to completely reorganize a computer's file system and Obsidian vault using the PARA (Projects, Areas, Resources, Archive) methodology combined with Zettelkasten principles for note-taking.

## Context

The user wants a hyper-organized digital life with:
- Clear folder structure for all files
- Consistent naming conventions
- Optimized Obsidian vault for knowledge management
- Automated-looking workflows
- Comprehensive user documentation

## Starting Locations (Replace these paths with actual paths)

- MOUNT_PATH: "/path/to/your/cloud/mount/or/external/drive/" (e.g., rclone mount, Google Drive, Dropbox)
- DOCUMENTS_PATH: "/path/to/Documents/" (local Documents folder)
- DOWNLOADS_PATH: "/path/to/Downloads/" (local Downloads folder)
- VAULT_PATH: "/path/to/your/Obsidian/vault/" (Obsidian vault location)
- BACKUP_PATH: "/path/to/backup/location/" (where to store pre-organization backups)
- PROJECTS_ORG: "path/to/organization/documentation/" (folder with research docs if available)

## Phase 1: PRE-EXECUTION BACKUP (CRITICAL)

Before doing ANYTHING else:

1. Create backup directory structure:
   - {BACKUP_PATH}/gdrive-mount/
   - {BACKUP_PATH}/documents/
   - {BACKUP_PATH}/downloads/
   - {BACKUP_PATH}/vault/

2. Backup ALL locations using rsync or cp:
   - Full copy of MOUNT_PATH
   - Full copy of DOCUMENTS_PATH  
   - Full copy of DOWNLOADS_PATH
   - Full copy of VAULT_PATH

3. Verify backups completed before proceeding

## Phase 2: FOLDER STRUCTURE CREATE

Create PARA folders in MOUNT_PATH:

00_INBOX/          - Temporary drop zone, process daily
01_PROJECTS/       - Active time-bound deliverables
02_AREAS/         - Ongoing responsibilities
03_RESOURCES/      - Reference material
04_ARCHIVE/       - Completed/obsolete items
90_TEMPLATES/     - Reusable templates
99_SYSTEM/        - Rules and documentation

Sub-folders for 01_PROJECTS:
- Project1/ (e.g., Business, Client Work)
- Project2/ (e.g., Career Search)
- Project3/ (e.g., Game Dev)

Sub-folders for 02_AREAS:
- Health/
- Finance/
- Home/
- Learning/
- Personal/

Sub-folders for 03_RESOURCES:
- AI/
- Tech/
- Career/
- Development/
- Media/
- Reading/
- Tools/

## Phase 3: VAULT STRUCTURE CREATE

In VAULT_PATH, create:

00_HOME/              - Entry points
├── Home.md           - START HERE (vault index)
├── Action Dashboard.md - Today's tasks
├── Parking Lot.md    - Unprocessed ideas
├── MOC_Index.md     - Topic index
└── Inbox Processing Checklist.md

01_PROJECTS/          - Project notes
├── Project1/
│   ├── Project1_MOC.md
│   └── [sub-notes]
├── Project2/
│   ├── Project2_MOC.md
│   └── [sub-notes]
└── ...

02_AREAS/            - Area dashboards
├── Health/
│   ├── Health Dashboard.md
│   └── [health notes]
├── Finance/
├── Learning/
├── Home/
└── Personal/

03_RESOURCES/         - Reference notes
├── AI/
├── Tech/
├── Career/
└── Development/

04_LOGS/
├── Daily/
└── Weekly/

90_TEMPLATES/        - Note templates

99_SYSTEM/          - Vault rules
├── File Naming Rules.md
├── Tag Rules.md
└── Vault Rules.md

## Phase 4: FILE MIGRATION

Move existing folders into new structure:

1. Archives/ → 04_ARCHIVE/
2. Work/ → 01_PROJECTS/
3. Personal/ → 02_AREAS/Personal/
4. Food/ → 02_AREAS/Home/
5. Media/ → 03_RESOURCES/Media/
6. Utilities/ → 03_RESOURCES/Tools/
7. Documents/ contents → 01_PROJECTS/ or relevant folder

## Phase 5: NAMING CONVENTIONS

Apply consistent naming:

Pattern: YYYY-MM-DD__context__description__vNN.ext

Examples:
- 2026-04-25__project__document-name__v01.pdf
- 2026-04-24__career__resume__v01.docx
- 2026-04-20__project__meeting-notes__v01.md

Rules:
1. Date first (ISO format for sorting)
2. Context/project slug (consistent lowercase)
3. Description (lowercase, hyphens)
4. Version (v01, v02, etc.)
5. NO SPACES - use hyphens or underscores
6. NO special characters

## Phase 6: CREATE SYSTEM FILES

Create these reference documents in 99_SYSTEM/:

### File Naming Rules.md
Standard naming pattern, examples, common slugs, anti-patterns to avoid.

### Tag Rules.md
Nested tag structure:
- type/* (meeting, daily, project, area, resource)
- status/* (inbox, active, pending, archived)
- project/* (your projects)
- topic/* (topics)

### Vault Rules.md
Folder structure explanation, daily workflow, key plugins.

## Phase 7: CREATE USER GUIDE

Create comprehensive File_System_User_Guide.md in 99_SYSTEM/ including:
- Philosophy (why this works)
- Directory structure (with tables)
- Naming conventions (with examples)
- Vault guide (entry points, views)
- Daily workflows (morning, during, evening, weekly)
- Tagging system
- Migration reference
- Troubleshooting
- Quick reference cards
- Maintenance schedule

## Phase 8: OBSIDIAN SETUP

If Obsidian vault is new/in.EMPTY:

1. Enable core plugins:
   - Daily Notes
   - Templates
   - Backlinks
   - Graph View

2. Configure Daily Notes:
   - Format: YYYY-MM-DD
   - Location: 04_LOGS/Daily/

3. Create templates in 90_TEMPLATES/:
   - Meeting template
   - Daily Note template
   - Project MOC template
   - Area Dashboard template

## Phase 9: VERIFICATION

Verify:
1. All backups exist
2. New folder structure in place
3. Files migrated logically
4. Naming conventions applied
5. System files created
6. User guide accessible

## Daily Workflow (to document)

Morning (5 min):
- Open Home.md
- Check Action Dashboard
- Review 3 priority tasks

During Day:
- New idea → Parking Lot.md first
- Complete task → Check off, add note
- Meeting → Project folder with template
- Research → Add to Resources

Evening (5 min):
- Review Action Dashboard
- Move Parking Lot items
- Update tomorrow's priorities

Weekly (30 min):
- Weekly Review
- Update MOCs
- Archive completed
- Tag cleanup

## Constraints

- BACKUP BEFORE ANYTHING
- NO deletion without explicit permission
- Create before migrate
- Document all changes
- Preserve important metadata

## Deliverables Checklist

- [ ] Pre-execution backups verified
- [ ] PARA folder structure created
- [ ] Files migrated to new structure
- [ ] Naming conventions applied
- [ ] Vault structure in place
- [ ] System files created (3 rules docs)
- [ ] Comprehensive user guide created
- [ ] Workflows documented
- [ ] Verification complete
```

---

## Execution Instructions for AI

When running this prompt, the AI should:

1. **First**: Read this prompt and ask for clarification on paths
2. **Then**: Execute Phase 1 (backup) - MOST CRITICAL
3. **Proceed**: Phase by phase through Phase 9
4. **Report**: Progress after each major step
5. **Ask**: Before any destructive action

### Sample Initial Response

The AI should respond with:

```
I'll help you reorganize your file system using PARA + Zettelkasten methodology. 

Before I begin, please confirm/provide:

1. MOUNT_PATH: Where is your main cloud/storage mounted?
2. VAULT_PATH: Where is your Obsidian vault?
3. BACKUP_PATH: Where should I store backups?
4. Any specific projects to create folders for?
5. Any sensitive files I should NOT touch?

Once confirmed, I'll:
1. Create backups first (required)
2. Build out PARA structure
3. Migrate files logically
4. Set up Obsidian vault
5. Create full documentation

Ready to proceed when you are.
```

---

## Success Criteria

The system is working when:
- [ ] Files follow naming pattern
- [ ] Everything has a clear home
- [ ] User can find anything in <30 seconds
- [ ] Daily workflow takes <10 minutes
- [ ] Weekly maintenance is manageable
- [ ] System is self-documenting
- [ ] User guide answers questions

---

*This prompt can be given to any capable AI agent to execute the complete methodology on any computer.*