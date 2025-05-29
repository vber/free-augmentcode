from utils.paths import get_home_dir, get_app_data_dir, get_storage_path, get_db_path, get_machine_id_path,get_workspace_storage_path
from augutils.json_modifier import modify_telemetry_ids
from augutils.sqlite_modifier import clean_augment_data
from augutils.workspace_cleaner import clean_workspace_storage

if __name__ == "__main__":
    print("System Paths:")
    print(f"Home Directory: {get_home_dir()}")
    print(f"App Data Directory: {get_app_data_dir()}")
    print(f"Storage Path: {get_storage_path()}")
    print(f"DB Path: {get_db_path()}")
    print(f"Machine ID Path: {get_machine_id_path()}")
    print(f"Workspace Storage Path: {get_workspace_storage_path()}")
    
    print("\nModifying Telemetry IDs:")
    try:
        result = modify_telemetry_ids()
        print("\nBackup created at:")
        print(f"Storage backup path: {result['storage_backup_path']}")
        if result['machine_id_backup_path']:
            print(f"Machine ID backup path: {result['machine_id_backup_path']}")
        
        print("\nOld IDs:")
        print(f"Machine ID: {result['old_machine_id']}")
        print(f"Device ID: {result['old_device_id']}")
        
        print("\nNew IDs:")
        print(f"Machine ID: {result['new_machine_id']}")
        print(f"Device ID: {result['new_device_id']}")
        
        print("\nCleaning SQLite Database:")
        db_result = clean_augment_data()
        print(f"Database backup created at: {db_result['db_backup_path']}")
        print(f"Deleted {db_result['deleted_rows']} rows containing 'augment' in their keys")
        
        print("\nCleaning Workspace Storage:")
        ws_result = clean_workspace_storage()
        print(f"Workspace backup created at: {ws_result['backup_path']}")
        print(f"Deleted {ws_result['deleted_files_count']} files from workspace storage")
        
        print("Now you can run VS Code and login with the new email.")
    except FileNotFoundError as e:
        print(f"Error: {e}")