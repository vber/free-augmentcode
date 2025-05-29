import os
import shutil
import time
import zipfile
import stat
from utils.paths import get_workspace_storage_path
from pathlib import Path

def remove_readonly(func, path, excinfo):
    """Handle read-only files and directories during deletion"""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        return False
    return True

def force_delete_directory(path: Path) -> bool:
    """
    Force delete a directory and all its contents.
    Returns True if successful, False otherwise.
    """
    try:
        if os.name == 'nt':
            # For Windows, handle read-only files and use long path
            path_str = '\\\\?\\' + str(path.resolve())
            shutil.rmtree(path_str, onerror=remove_readonly)
        else:
            shutil.rmtree(path, onerror=remove_readonly)
        return True
    except Exception:
        return False

def clean_workspace_storage() -> dict:
    """
    Cleans the workspace storage directory after creating a backup.
    
    This function:
    1. Gets the workspace storage path
    2. Creates a zip backup of all files in the directory
    3. Deletes all files in the directory
    
    Returns:
        dict: A dictionary containing operation results
        {
            'backup_path': str,
            'deleted_files_count': int
        }
    """
    workspace_path = get_workspace_storage_path()
    
    if not os.path.exists(workspace_path):
        raise FileNotFoundError(f"Workspace storage directory not found at: {workspace_path}")
    
    # Convert to Path object for better path handling
    workspace_path = Path(workspace_path)
    
    # Create backup filename with timestamp
    timestamp = int(time.time())
    backup_path = f"{workspace_path}_backup_{timestamp}.zip"
    
    # Create zip backup
    failed_compressions = []
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in workspace_path.rglob('*'):
            if file_path.is_file():
                try:
                    file_path_str = str(file_path)
                    if os.name == 'nt':
                        file_path_str = '\\\\?\\' + str(file_path.resolve())
                    
                    arcname = file_path.relative_to(workspace_path)
                    zipf.write(file_path_str, str(arcname))
                except (OSError, PermissionError, zipfile.BadZipFile) as e:
                    failed_compressions.append({
                        'file': str(file_path),
                        'error': str(e)
                    })
                    continue
    
    # Count files before deletion
    total_files = sum(1 for _ in workspace_path.rglob('*') if _.is_file())
    
    # Delete all files in the directory
    failed_operations = []
    
    def handle_error(e: Exception, path: Path, item_type: str):
        failed_operations.append({
            'type': item_type,
            'path': str(path),
            'error': str(e)
        })

    # First attempt: Try to delete the entire directory tree at once
    if not force_delete_directory(workspace_path):
        # If bulk deletion fails, try the file-by-file approach
        # Delete files first
        for file_path in workspace_path.rglob('*'):
            if file_path.is_file():
                try:
                    # Clear read-only attribute if present
                    if os.name == 'nt':
                        file_path_str = '\\\\?\\' + str(file_path.resolve())
                        os.chmod(file_path_str, stat.S_IWRITE)
                    else:
                        os.chmod(str(file_path), stat.S_IWRITE)
                    
                    file_path.unlink(missing_ok=True)
                except (OSError, PermissionError) as e:
                    handle_error(e, file_path, 'file')

        # Delete directories from deepest to root
        dirs_to_delete = sorted(
            [p for p in workspace_path.rglob('*') if p.is_dir()],
            key=lambda x: len(str(x).split(os.sep)),
            reverse=True
        )
        
        for dir_path in dirs_to_delete:
            try:
                # Try force delete first
                if not force_delete_directory(dir_path):
                    # If force delete fails, try regular delete
                    if os.name == 'nt':
                        dir_path_str = '\\\\?\\' + str(dir_path.resolve())
                        os.rmdir(dir_path_str)
                    else:
                        dir_path.rmdir()
            except (OSError, PermissionError) as e:
                handle_error(e, dir_path, 'directory')
    
    return {
        'backup_path': str(backup_path),
        'deleted_files_count': total_files,
        'failed_operations': failed_operations,
        'failed_compressions': failed_compressions
    } 