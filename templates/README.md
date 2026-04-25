# Template Pack

Ready-to-use templates for file-org-wiz organization.

## Templates

| Template | Purpose | Location |
|----------|---------|-----------|
| Meeting Notes | Project meetings | `01_meeting.md` |
| Daily Note | Daily logging | `02_daily.md` |
| Project MOC | Project hub/index | `03_project_moc.md` |
| Area Dashboard | Area overview | `04_area_dashboard.md` |
| Project Note | Individual project notes | `05_project_note.md` |

## Using Templates

### Copy to Your Vault

```bash
# Copy all templates
cp templates/*.md /path/to/vault/90_TEMPLATES/

# Or individual template
cp templates/01_meeting.md /path/to/vault/90_TEMPLATES/
```

### Use in Obsidian

1. Copy template to `90_TEMPLATES/`
2. Use Templates plugin: `Ctrl+P` > "Insert template"
3. Fill in placeholders

### Placeholders

| Placeholder | What to Enter |
|-------------|----------------|
| `{{date}}` | Current date: YYYY-MM-DD |
| `{{title}}` | Title of note |
| `{{project}}` | Project name |
| `{{slug}}` | Project slug (lowercase, hyphens) |
| `{{area}}` | Area name |

## Customizing

Edit templates directly or create variants:

- `01_meeting__client.md` - Client-specific meetings
- `02_daily__work.md` - Work-focused daily

---

## Template Best Practices

1. Keep frontmatter complete
2. Use consistent placeholders
3. Include status for tracking
4. Add tags for searchability