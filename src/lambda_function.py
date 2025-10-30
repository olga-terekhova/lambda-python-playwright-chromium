import boto3
import importlib.util
import os
import traceback


def handler(event, context):
    """
    Expected event structure:
    {
        "Bucket": "my-lambda-scripts",
        "Key": "scripts/user_script.py",
        "EntryFunction": "main",
        "Parameters": { "param1": "value1", "param2": 42 }
    }
    """
    
    # --- 1. Validate input ---
    try:
        bucket = event["Bucket"]
        key = event["Key"]
    except KeyError as e:
        raise ValueError(f"Missing required field in event: {e}")

    entry_func_name = event.get("EntryFunction", "main")
    params = event.get("Parameters", {})

    # --- 2. Prepare local temp path ---
    local_path = f"/tmp/{os.path.basename(key)}"
    print(local_path)

    s3 = boto3.client("s3")
    
    # --- 3. Download the Python script ---
    print(f"Downloading {key} from S3 bucket {bucket}...")
    try:
        s3.download_file(bucket, key, local_path)
    except Exception as e:
        raise RuntimeError(f"Failed to download {key} from {bucket}: {e}")
    
    # --- 4. Dynamically load the module ---
    module_name = os.path.splitext(os.path.basename(local_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, local_path)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        tb = traceback.format_exc()
        raise RuntimeError(f"Failed to load module {module_name}:\n{tb}")
    

    # --- 5. Execute the specified entry function ---
    if not hasattr(module, entry_func_name):
        raise AttributeError(f"Module {module_name} does not define function '{entry_func_name}'")

    func = getattr(module, entry_func_name)

    # Ensure params is a dict; pass as keyword arguments
    if not isinstance(params, dict):
        raise TypeError("Parameters field must be a JSON object (dictionary)")

    print(f"Executing {entry_func_name}({params})...")
    try:
        result = func(**params)
    except Exception as e:
        tb = traceback.format_exc()
        raise RuntimeError(f"Error executing function '{entry_func_name}':\n{tb}")

    # --- 6. Return result ---
    print(f"Execution completed successfully.")
    return {"Result": result}

