import os
import re

backend_dir = r"E:\Gen Ai Project\ai company\backend"

for root, dirs, files in os.walk(backend_dir):
    if ".venv" in dirs:
        dirs.remove(".venv")
    if "__pycache__" in dirs:
        dirs.remove("__pycache__")
        
    for file in files:
        if file.endswith(".py") and file != "fix_imports.py":
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            rel_path = os.path.relpath(filepath, backend_dir)
            parts = rel_path.split(os.sep)[:-1]
            
            def replacer(match):
                dots = match.group(1)
                module = match.group(2)
                
                num_dots = len(dots)
                if num_dots == 1:
                    base = parts
                else:
                    base = parts[:-(num_dots-1)] if (num_dots-1) <= len(parts) else []
                
                base_str = ".".join(base)
                if base_str and module:
                    new_module = f"{base_str}.{module}"
                elif base_str:
                    new_module = base_str
                else:
                    new_module = module
                    
                return f"from {new_module} import"
            
            new_content = re.sub(r'from (\.+)([a-zA-Z0-9_.]*) import', replacer, content)
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed {rel_path}")
