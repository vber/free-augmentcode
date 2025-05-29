import json
import os
import time
import shutil
from utils.paths import get_storage_path, get_machine_id_path
from utils.device_codes import generate_machine_id, generate_device_id

def _create_backup(file_path: str) -> str:
    """
    Creates a backup of the specified file with timestamp.
    
    Args:
        file_path (str): Path to the file to backup
        
    Returns:
        str: Path to the backup file
        
    Format: <filename>.bak.<timestamp>
    """
    timestamp = int(time.time())
    backup_path = f"{file_path}.bak.{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def modify_telemetry_ids() -> dict:
    """
    Modifies the telemetry IDs in the VS Code storage.json file and machine ID file.
    Creates backups before modification.
    
    This function:
    1. Creates backups of the storage.json and machine ID files
    2. Reads the storage.json file
    3. Generates new machine and device IDs
    4. Updates the telemetry.machineId and telemetry.devDeviceId values in storage.json
    5. Updates the machine ID file with the new machine ID
    6. Saves the modified files
    
    Returns:
        dict: A dictionary containing the old and new IDs and backup information
        {
            'old_machine_id': str,
            'new_machine_id': str,
            'old_device_id': str,
            'new_device_id': str,
            'storage_backup_path': str,
            'machine_id_backup_path': str
        }
    """
    storage_path = get_storage_path()
    machine_id_path = get_machine_id_path()
    
    if not os.path.exists(storage_path):
        raise FileNotFoundError(f"Storage file not found at: {storage_path}")
    
    # Create backups before modification
    storage_backup_path = _create_backup(storage_path)
    machine_id_backup_path = None
    if os.path.exists(machine_id_path):
        machine_id_backup_path = _create_backup(machine_id_path)
    
    # Read the current JSON content
    with open(storage_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Store old values
    old_machine_id = data.get('telemetry.machineId', '')
    old_device_id = data.get('telemetry.devDeviceId', '')
    
    # Generate new IDs
    new_machine_id = generate_machine_id()
    new_device_id = generate_device_id()
    
    # Update the values in storage.json
    data['telemetry.machineId'] = new_machine_id
    data['telemetry.devDeviceId'] = new_device_id
    
    # Write the modified content back to storage.json
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    # Write the new machine ID to the machine ID file
    with open(machine_id_path, 'w', encoding='utf-8') as f:
        f.write(new_device_id)
    
    return {
        'old_machine_id': old_machine_id,
        'new_machine_id': new_machine_id,
        'old_device_id': old_device_id,
        'new_device_id': new_device_id,
        'storage_backup_path': storage_backup_path,
        'machine_id_backup_path': machine_id_backup_path
    } 