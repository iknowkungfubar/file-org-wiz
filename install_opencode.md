# OpenCode Skill Integration

## Using file-org-wiz with OpenCode/OpenCode

OpenCode uses a skill system. Here's how to integrate file-org-wiz:

### Install the Skill

Copy the skill file to OpenCode's skills directory:

```bash
# Create skills directory
mkdir -p ~/.opencode/skills/file-org-wiz

# Copy skill file
cp /path/to/file-org-wiz/SKILL.md ~/.opencode/skills/file-org-wiz/SKILL.md
```

### Alternative: Direct Link

If your file-org-wiz repo is in a consistent location, create a symlink:

```bash
ln -s /path/to/file-org-wiz/SKILL.md ~/.opencode/skills/file-org-wiz/SKILL.md
```

### Verify Installation

```bash
ls -la ~/.opencode/skills/file-org-wiz/
```

You should see:
```
SKILL.md -> /path/to/file-org-wiz/SKILL.md
```

### Update OpenCode Config (if needed)

Some OpenCode versions need explicit skill registration. Create `~/.opencode/config.json`:

```json
{
  "skills": {
    "file-org-wiz": {
      "path": "~/.opencode/skills/file-org-wiz/SKILL.md",
      "enabled": true
    }
  }
}
```

### Using the Skill

In OpenCode, just say:

```
Use file-org-wiz skill to reorganize my files at /your/mount/path
```

Or load the skill explicitly:

```
/skill file-org-wiz
```

The skill will:
1. Ask for your paths (mount, vault, backup)
2. Execute the full reorganization
3. Create user documentation

### Skill Metadata

The skill provides these triggers:

| Trigger Words | Action |
|--------------|--------|
| reorganize files | Run full reorganization |
| organize computer | Run full reorganization |
| PARA structure | Create folder structure |
| Obsidian vault | Set up vault |

### Customization

To customize paths, edit the skill file:

```markdown
## Default Paths (edit these)

- MOUNT_PATH: "/your/default/mount"
- VAULT_PATH: "/your/default/vault"
- BACKUP_PATH: "/your/default/backup"
```

---

## Troubleshooting

### Skill not Loading

1. Check path: `ls -la ~/.opencode/skills/file-org-wiz/`
2. Check permissions: `chmod 644 ~/.opencode/skills/file-org-wiz/SKILL.md`
3. Check format: First line must be `# Skill: File Organization Wizard`

### Paths Not Working

Use absolute paths. The skill uses bash commands which need full paths:
- ❌ `~/Documents` 
- ✅ `/home/username/Documents`

### MCP Server Conflicts

If using both skill and MCP server, ensure different ports: