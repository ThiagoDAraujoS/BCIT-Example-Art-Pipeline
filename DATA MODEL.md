# Asset Library Data Model

## Overview

The project implements a show management tool with a node-based file system that addresses the complex interconnectivity of art assets prevalent in the Game and Movie industries. In these creative domains, 3D models often rely on materials, textures, shaders, and master shaders, forming intricate relationships between assets. Traditional acyclic tree structures fall short in effectively capturing and expressing these asset connections. To overcome this limitation, the data model design introduces a more expressive and flexible folder structure that accurately describes the dynamic relationships between assets.

The central components of the project's API are the `Show Manager` and the `Asset Library`. Show Managers are equipped with an Asset Library and are responsible for generating `Show` objects, each comprising a set of `Shot` assets. The `Show Manager` leverages the `Asset Library` to request the generation of new `Shot Assets` for the shows.

The `Asset Library` is the backbone of the system, providing a node-based folder structure that organizes asset objects and their designated folders. Assets are represented as nodes capable of binding themselves to other assets, establishing resource requisition chains where one asset may require another asset to function effectively. This design approach facilitates the seamless management of complex asset relationships within the entertainment projects.

## Description

## Show Manager
The show manager simply manages `Shows`, and provide a set of tools to create, edit and delete them. `Shows` are stored in a `dictionary`, where the show name acts as the key and the value is a `Show Dataclass` object. The `Show Manager` provides the necessary methods to access and manipulate this data structure.

## Asset Library
The `Asset Library` is a fundamental component of the show management tool, responsible for managing and organizing assets efficiently. It utilizes a node-based structure for assets, which enables effective tracking and retrieval of assets based on their relationships. The `Asset Library` also provides redundant indexing to ensure quick access to assets, while Save Files guarantee data persistence, and Folder objects simplify file system management, contributing to a robust and functional asset management system.

##### Asset Representation
- Assets in the `Asset Library` are stored in a dictionary that maps each asset's `UUID` to its corresponding `Dataclass` object.
- Each asset is represented as a doubly linked node, allowing it to establish connections with other assets. This doubly linked nature enables assets to track both the assets they use and the assets that use them.
- Assets express their connections through `UUIDs`, which means that clients obtaining an asset's link to another asset must check with the `Asset Library` to access the actual linked asset's object representation.
- The implementation leverages this technique to decompose the recursive nature of assets as nodes into a simple `UUID` dictionary, enhancing simplicity and efficiency.

##### Asset Types and Metadata
- Assets are implemented as simple `dataclasses`, providing a clean and organized structure for asset data.
- Specialized asset types, such as `Music Assets`, `Shot Assets`, and `Texture Assets`, inherit from the base asset class and include additional metadata information specific to their respective asset types.
  
##### Double Indexing for Efficient Querying
- The `Asset Library` employs a double indexing feature to optimize querying assets based on their types. Newly generated assets are organized in a table of `asset_types`, where each asset type is associated with a set containing all assets of that type.
- Likewise `Asset`s are doubly linked for the same reason. And they are similarly managed by the library, witch ensures the proper asset linking and unlinking.

### Save Files
`Save File` objects keep track of a `JSON` file and a reference to a `dataclass_json` decorated object. When the `save` method is invoked, all data stored in the reference is recorded to the `JSON` file. When the `load` method is invoked, the reference is updated with the recorded values. The `Save File` also provides a decorator named `autosave`, which automatically triggers `save` upon completion of any method tagged with it.

### Folders
`Folder` objects are used to control a directories its subdirectories. Once a `Folder` object is created, it ensures the creation of an directory, and it can create, delete, and archive subdirectories upon request. Both the Show Manager and Asset Library utilize Folder Objects extensively, as each asset and show requires its own folder.