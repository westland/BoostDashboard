import os
import zipfile

def create_release_zip(zip_name="WoWBoost_Release.zip"):
    # Target directory is the project root (where this script is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(current_dir, zip_name)
    
    print(f"[Package] Packaging project release bundle: {zip_name}...")
    
    # Exclude directories
    exclude_folders = {".venv", "venv", ".git", "__pycache__", "build", "dist"}
    # Exclude active sensitive credentials or local databases
    exclude_files = {".env", "wow_leads.json", zip_name, "WoWBoost_Release.zip"}
    
    file_count = 0
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(current_dir):
                # Modify dirs in-place to prevent os.walk from recursing into excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_folders]
                
                for file in files:
                    if file in exclude_files:
                        continue
                    if file.endswith(('.pyc', '.pyo', '.gitkeep')):
                        continue
                        
                    file_path = os.path.join(root, file)
                    # Create relative path in the archive
                    rel_path = os.path.relpath(file_path, current_dir)
                    zipf.write(file_path, rel_path)
                    file_count += 1
                    
        print(f"[Success] Successfully archived {file_count} files into {zip_path}")
        return zip_path
    except Exception as e:
        print(f"[Error] Failed to build zip archive: {e}")
        return None

if __name__ == "__main__":
    create_release_zip()
