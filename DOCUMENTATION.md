## Overview

The Show Manager is designed to utilize an instance of the Asset Library, enabling it to generate shots as assets and bind them to shows. Additionally, any new asset can be created directly using the Asset Library through the Show Manager. This design choice ensures that the Asset Library remains integrated with the Show Manager, and both components work seamlessly together to manage assets effectively. However, if required, the Asset Library can still be used independently in other applications.

With the objective of building a server on top of the API, the old Proxy script no longer exists. As a result, to access the API's functionalities, you can use the `ShowManager` and `AssetLibrary` objects directly.
## Setup
Here's how you can set up these objects in order to work with the API:

```python
from ShowSafari.show_manager import ShowManager  
from ShowSafari.asset_library import AssetLibrary

path = "[Path to any existing folder]"
library = AssetLibrary(path)  
manager = ShowManager(path, library)
```

By instantiating objects of type `library` and `manager`, the folders for both the library and the show manager will be set up. You can use different paths for the manager and library if needed.

You can then use these objects' methods to perform the required operations. Here's a breakdown.

# SHOW MANAGER
### Create & Delete Show
These commands will create and delete a show instance along with their folders.

```python
manager.create_show("My Show Name")
manager.delete_show("My Show Name")
```

### Get & Set Show Data
These methods work with JSON strings and are designed to be used by external UI applications. If you want to get and set the show attributes in a more human-friendly way, use the _`Get Show Instance` (see below)_.

```python
json_string = manager.get_show_data("My Show Name")
manager.set_show_data("My Show Name", '{"key": "value"}')
```

### Get Show Instance, Folder, and Names
```python
show_instance = manager["My Show Name"]
show_folder_path = manager.get_show_folder("My Show Name")
shows_names = manager.get_show_names()
```

### Create & Delete Shot
These methods will create and delete shots entirely. Deleting a shot will remove it from all shows and the library. It is not advised to remove shots using the library directly, as the manager will not be aware they have been removed, leading to potential missing links.

```python
shot_UUID_string = manager.create_shot("My Show Name", "New Shot")
manager.delete_shot("My Show Name", shot_UUID_string)
```

### Add & Remove Shot
These methods add and remove shots from a show's shot dependency list. Shots are not deleted when removed, so even if no show uses a shot, the library will still retain it.

```python
manager.add_shot("My Show Name", shot_UUID_string)
manager.remove_shot("My Show Name", shot_UUID_string)
```

# ASSET LIBRARY

All assets in the library are accessed through their UUIDs. While this design choice may not be very human-friendly, it aligns with the major intention behind this API - to provide the necessary functionalities for a UI application to manage assets. Most methods in this object require a valid UUID, and there are no error-handling features to protect users from inputting non-existent UUIDs into the system.

### Create & Remove Asset
These commands will create and delete an asset instance along with its folders.

```python
asset_uuid = library.create(asset_name="My Asset Name", asset_type="Music")
library.delete(asset_uuid)
```

### Archive & Unpack Asset
These commands will zip and unzip assets. Archives are immutable, and several methods return errors if the client attempts to modify an archive.

```python
library.archive(asset_uuid)
library.unpack(asset_uuid)
```

### Connect & Disconnect Assets
These commands will link two assets together.

```python
library.connect(parent_uuid, child_uuid)
library.disconnect(parent_uuid, child_uuid)
```

### Get & Set Asset Data
These methods work with JSON strings and are designed for use by external UI applications. If you prefer a more human-friendly approach to get and set asset attributes, use the _`Get Asset Instance` (see below)_.

```python
json_string = library.get_data(asset_uuid)
library.set_data(asset_uuid, '{"key": "value"}')
```

### Get Library Information
There are many other methods to fetch data from the library and its assets. Here's a quick rundown of those.

```python
asset_uuid = "be42c2cc-09e5-4c99-9337-a0291987bce8"

# Get asset instance
asset_instance = library[asset_uuid]

# Check if asset exists
if library.exists(asset_uuid):
    pass

# Get a set of all asset types
asset_type_list = library.get_types(asset_uuid)

# Get a set containing all assets
assets = library.get_all_assets(asset_uuid)

# Get a set containing all assets of a type
shots = library.get_all_assets_of_type(asset_uuid, "Shots")

# Get a set containing all assets named "xxx"
assets_named_xxx = library.get_by_name("xxx")
```