# Scanner module - deep file scanning and analysis

from __future__ import annotations

import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict, List


# File type to PARA category mapping
FILE_TYPE_CATEGORIES = {
    # Projects - time-bound deliverables
    "01_PROJECTS": [
        ".psd", ".ai", ".sketch", ".fig", ".xd",
        ".proto", ".storyboard", ".xcodeproj",
    ],
    # Areas - ongoing responsibilities
    "02_AREAS": [
        ".budget", ".xlsx", ".csv",
    ],
    # Resources - reference material
    "03_RESOURCES": [
        ".pdf", ".epub", ".mobi",
        ".md", ".txt", ".notes",
        ".url", ".bookmarks",
    ],
    # Archive
    "04_ARCHIVE": [
        ".zip", ".tar", ".gz", ".7z", ".rar",
    ],
}


# Patterns that suggest a category
NAME_PATTERNS = {
    "01_PROJECTS": [
        r"project", r"proposal", r"draft", r"v\d", r"final",
        r"client", r"contract",
    ],
    "02_AREAS": [
        r"invoice", r"tax", r"budget", r"health", r"fitness",
        r"finance", r"投资", r"预算",
    ],
    "03_RESOURCES": [
        r"reference", r"note", r"research", r"article",
        r"tutorial", r"guide", r"documentation",
    ],
    "04_ARCHIVE": [
        r"archive", r"old", r"backup", r"completed", r"done",
    ],
}


def scan_files_recursive(base_path, max_depth=10, include_hidden=False):
    """Recursively scan all files in directory."""
    files = []
    
    try:
        for root, dirs, filenames in os.walk(base_path):
            # Calculate depth
            rel_root = os.path.relpath(root, base_path)
            depth = rel_root.count(os.sep) if rel_root != '.' else 0
            
            if depth >= max_depth:
                continue
            
            # Filter hidden directories if needed
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in filenames:
                # Skip hidden files if needed
                if not include_hidden and filename.startswith('.'):
                    continue
                
                file_path = os.path.join(root, filename)
                
                try:
                    stat = os.stat(file_path)
                    files.append({
                        "path": file_path,
                        "name": filename,
                        "extension": Path(filename).suffix.lstrip('.').lower(),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "depth": depth + 1,
                    })
                except (OSError, IOError):
                    continue
                    
    except OSError:
        pass
    
    return files


def classify_by_extension(extension):
    """Classify file to PARA category by extension."""
    extension = extension.lower().lstrip('.')
    
    # Check file type categories with dots (we're comparing stripped extension)
    ext_with_dot = f".{extension}"
    for category, extensions in FILE_TYPE_CATEGORIES.items():
        if ext_with_dot in extensions:
            return category
    
    # Also check direct extensions in the categories
    for category, extensions in FILE_TYPE_CATEGORIES.items():
        if extension in extensions:
            return category
    
    return "03_RESOURCES"  # Default to Resources


def classify_by_name(filename):
    """Classify file to PARA category by filename patterns."""
    filename_lower = filename.lower()
    
    for category, patterns in NAME_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, filename_lower, re.IGNORECASE):
                return category
    
    return None


def classify_by_date(modified):
    """Classify file by age - older than 6 months goes to Archive."""
    try:
        mod_date = datetime.fromisoformat(modified)
        age_days = (datetime.now() - mod_date).days
        
        if age_days > 180:  # 6 months
            return "04_ARCHIVE"
    except (ValueError, OSError):
        pass
    
    return None


def classify_file(file_info, use_date=True):
    """Classify a file to suggested PARA category."""
    extension_category = classify_by_extension(file_info.get("extension", ""))
    name_category = classify_by_name(file_info.get("name", ""))
    date_category = classify_by_date(file_info.get("modified", "")) if use_date else None
    
    # Priority: name > extension > date
    if date_category == "04_ARCHIVE" and not name_category:
        return {
            "category": "04_ARCHIVE",
            "confidence": "medium",
            "reason": "file is older than 6 months"
        }
    
    if name_category:
        return {
            "category": name_category,
            "confidence": "high",
            "reason": f"filename matches {name_category} pattern"
        }
    
    if extension_category:
        return {
            "category": extension_category,
            "confidence": "medium",
            "reason": f"file type suggests {extension_category}"
        }
    
    return {
        "category": "03_RESOURCES",
        "confidence": "low",
        "reason": "default category"
    }


def scan_and_categorize(base_path, max_depth=10, use_date=True):
    """Deep scan and categorize all files in directory."""
    files = scan_files_recursive(base_path, max_depth)
    
    categorized = []
    summary = {
        "00_INBOX": 0,
        "01_PROJECTS": 0,
        "02_AREAS": 0,
        "03_RESOURCES": 0,
        "04_ARCHIVE": 0,
    }
    
    for file_info in files:
        classification = classify_file(file_info, use_date)
        file_info["category"] = classification["category"]
        file_info["confidence"] = classification["confidence"]
        file_info["reason"] = classification["reason"]
        
        categorized.append(file_info)
        
        cat = classification["category"]
        if cat in summary:
            summary[cat] += 1
    
    return {
        "base_path": base_path,
        "total_files": len(categorized),
        "files": categorized,
        "summary": summary,
    }


def get_file_hash(file_path, algorithm="sha256"):
    """Get file content hash."""
    try:
        hash_func = hashlib.new(algorithm)
        
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (OSError, IOError):
        return ""


def get_quick_hash(file_path):
    """Get quick hash (first + last 4KB)."""
    try:
        file_size = os.path.getsize(file_path)
        
        hash_func = hashlib.md5()
        
        with open(file_path, "rb") as f:
            # First 4KB
            hash_func.update(f.read(4096))
            
            # Last 4KB if file is large enough
            if file_size > 8192:
                f.seek(-4096, 2)
                hash_func.update(f.read(4096))
        
        return hash_func.hexdigest()
    except (OSError, IOError):
        return ""


# Default extension category mapping
EXT_TO_PARA = {
    # Design files -> Projects
    "psd": "01_PROJECTS",
    "ai": "01_PROJECTS",
    "sketch": "01_PROJECTS",
    "fig": "01_PROJECTS",
    "xd": "01_PROJECTS",
    "indd": "01_PROJECTS",
    "pptx": "01_PROJECTS",
    "key": "01_PROJECTS",
    
    # Documents often Projects
    "doc": "01_PROJECTS",
    "docx": "01_PROJECTS",
    
    # Finance -> Areas
    "xlsx": "02_AREAS",
    "csv": "02_AREAS",
    "numbers": "02_AREAS",
    
    # Resources
    "pdf": "03_RESOURCES",
    "md": "03_RESOURCES",
    "txt": "03_RESOURCES",
    "url": "03_RESOURCES",
    "epub": "03_RESOURCES",
    "mobi": "03_RESOURCES",
    
    # Archive
    "zip": "04_ARCHIVE",
    "tar": "04_ARCHIVE",
    "gz": "04_ARCHIVE",
}


def suggest_category(file_path):
    """Suggest PARA category based on file analysis."""
    path = Path(file_path)
    name = path.stem.lower()
    ext = path.suffix.lstrip('.').lower()
    
    # By extension
    if ext in EXT_TO_PARA:
        return EXT_TO_PARA[ext], f"extension: .{ext}"
    
    # By name patterns
    name_patterns = {
        "01_PROJECTS": ["project", "proposal", "draft", "client", "contract"],
        "02_AREAS": ["invoice", "tax", "budget", "finance", "health", "fitness"],
        "03_RESOURCES": ["note", "reference", "research", "reading"],
        "04_ARCHIVE": ["archive", "old", "backup", "completed"],
    }
    
    for cat, patterns in name_patterns.items():
        for pattern in patterns:
            if pattern in name:
                return cat, f"name pattern: {pattern}"
    
    # Default
    return "03_RESOURCES", "default"