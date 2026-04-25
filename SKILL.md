# Skill: File Organization Wizard

> Use when: reorganize files, organize computer, PARA structure, clean up folders, Obsidian vault setup, file management

## Description

This skill provides a complete file organization system using the PARA (Projects, Areas, Resources, Archive) methodology combined with Zettelkasten principles for Obsidian vaults. It guides through backup, folder structure creation, file migration, and documentation.

## How to Use

1. **Load the skill** - It provides the AI agent prompt and methodology
2. **The AI reads** - The prompt file contains detailed execution instructions
3. **User provides paths** - Mount point, vault path, backup location
4. **AI executes** - All 9 phases from backup through verification

## Files Provided

When loaded, this skill provides access to:

- `/path/to/skill/AI_File_Organization_Agent_Prompt.md` - The execution prompt
- `/path/to/skill/Why_PARA_Zettelkasten.md` - Methodology explanation

## Prompt the AI

After loading, say something like:

```
Use the file-org-wiz skill to reorganize my files at [YOUR_PATH]
```

## What Happens

The skill will:

1. Ask for path confirmation (mount, vault, backup locations)
2. Execute Phase 1: Backup (CRITICAL)
3. Create PARA folder structure
4. Migrate files to new structure
5. Set up Obsidian vault
6. Create system documentation
7. Build comprehensive user guide

## Requirements

An AI agent that can:
- Execute bash commands
- Read/write files
- Navigate directory structure

## Output Structure

```
MOUNT_PATH/
├── 00_INBOX/
├── 01_PROJECTS/
├── 02_AREAS/
├── 03_RESOURCES/
├── 04_ARCHIVE/
├── 90_TEMPLATES/
└── 99_SYSTEM/
    ├── File Naming Rules.md
    ├── Tag Rules.md
    ├── Vault Rules.md
    └── File_System_User_Guide.md
```

## Naming Conventions

Pattern: `YYYY-MM-DD__context__description__vNN.ext`

## Skill Metadata

- **name**: file-org-wiz
- **type**: automation/workflow
- **version**: 1.0.0
- **author**: TURIN