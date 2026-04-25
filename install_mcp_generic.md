# Generic MCP Client Integration

## Using file-org-wiz with Any MCP-Compatible Client

Many AI tools support MCP. Here's how to integrate with any:

### Universal MCP Setup

#### 1. Start the Server

```bash
cd /path/to/file-org-wiz
pip install flask
python mcp_server.py --port 5000 --mount /your/mount --backup /your/backup &
```

#### 2. Configure Your Client

**Basic HTTP Integration:**

```bash
# Check health
curl http://localhost:5000/health

# Create backup
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"source_path": "/mount", "backup_path": "/backup"}'

# Organize  
curl -X POST http://localhost:5000/organize \
  -H "Content-Type: application/json" \
  -d '{"mount_path": "/mount", "backup_path": "/backup"}'
```

### Clients That Support HTTP

| Client | Integration |
|--------|-----------|
| OpenAI Responses API | Use as tool function |
| LangChain | Use as Tool |
| LlamaIndex | Use as Tool |
| AutoGen | Use as custom tool |
| smolagents | Use as MCP proxy |

### LangChain Integration

```python
from langchain.tools import Tool
from langchain.agents import AgentType, initialize_agent
import requests

def organize_filesWrapper(query: str) -> str:
    """File organization wrapper"""
    response = requests.post(
        "http://localhost:5000/organize",
        json={"mount_path": query, "backup_path": "/data/backup"}
    )
    return response.json()

def get_structureWrapper(path: str) -> str:
    """Get directory structure"""
    response = requests.get(f"http://localhost:5000/structure?path={path}")
    return response.json()

organize_tool = Tool(
    name="file_organize",
    func=organize_filesWrapper,
    description="Organize files using PARA methodology"
)

structure_tool = Tool(
    name="file_structure", 
    func=get_structureWrapper,
    description="Get current directory structure"
)

# Add to agent
tools = [organize_tool, structure_tool]
agent = initialize_agent(tools, llm, AgentType.CONVERSATIONAL_REACT_DESCRIPTION)
```

### LlamaIndex Integration

```python
from llama_index.tools import FunctionTool
import requests

def organize_files(query: str):
    response = requests.post(
        "http://localhost:5000/organize",
        json={"mount_path": query, "backup_path": "/data/backup"}
    )
    return response.text

def get_structure(path: str):
    response = requests.get(
        f"http://localhost:5000/structure?path={path}"
    )
    return response.text

organize_tool = FunctionTool.from_defaults(organize_files)
structure_tool = FunctionTool.from_defaults(get_structure)

# Add to index
tools = [organize_tool, structure_tool]
```

### AutoGen Integration

```python
from autogen import ConversableAgent, Tool

def organize_files(query):
    import requests
    response = requests.post(
        "http://localhost:5000/organize",
        json={"mount_path": query, "backup_path": "/data/backup"}
    )
    return response.json()

organize_tool = Tool(
    name="organize_files",
    func=organization_files,
    description="Organize files using PARA methodology"
)

assistant = ConversableAgent(
    "assistant",
    llm_config={"tools": [organize_tool]}
)
```

### smolagents Integration

```python
from smolagents import CodeAgent, LiteLLMModel
from smolagents.tools import Tool

organize_tool = Tool(
    name="organize",
    func=lambda q: requests.post("http://localhost:5000/organize", json={"mount_path": q}).text,
    description="Organize files using PARA methodology"
)

agent = CodeAgent(tools=[organize_tool], model=LiteLLMModel("gpt-4"))
```

### OpenAI Responses API (Functions)

```json
{
  "name": "organize_files",
  "description": "Organize files using PARA methodology",
  "parameters": {
    "type": "object",
    "properties": {
      "mount_path": {
        "type": "string",
        "description": "Path to organize"
      },
      "backup_path": {
        "type": "string", 
        "description": "Backup location"
      }
    },
    "required": ["mount_path"]
  }
}
```

### Connecting Over Network

If MCP server is on a different machine:

```python
import requests

# Remote server
BASE_URL = "http://your-server:5000"

def organize_remote(mount_path: str, backup_path: str):
    response = requests.post(
        f"{BASE_URL}/organize",
        json={
            "mount_path": mount_path,
            "backup_path": backup_path,
            "do_backup": True
        }
    )
    return response.json()
```

---

## Troubleshooting

### Connection Refused

1. Check server: `curl localhost:5000/health`
2. Check firewall: Allow port 5000
3. Check Python: `pip list | grep flask`

### CORS Errors

Add CORS to Flask app:

```python
from flask_cors import CORS
CORS(app)
```

### Timeout

Increase timeout in requests:
```python
requests.post(url, timeout=300)
```