### Transition to Monolithic Metadata
The API's previous approach scattered data across multiple files and folders, specific to each show or asset. The new design consolidated all information into a single file, simplifying serialization. However, this made the entire library dependent on one file, risking disruptions due to corruption. While a metadata-rebuilding algorithm could mitigate this, it led to data loss. Ultimately, the fragmented approach proved more manageable and safer in the long run.

### Redundant Indexing for Performance Optimization
The API's design includes redundant indexing for enhanced performance. Various indexers, such as the type indexer table and double indexing in nodes, facilitate efficient data access. However, this optimization poses challenges. When creating, modifying, or deleting elements, additional operations are required to maintain the redundant indexing. Any corruption or unauthorized removal of indexes can lead to data structure coherence issues. To address this, meticulous design and well-encapsulated data managers are essential for maintaining effective redundancy.

### Transition to Aggregation-Based Design
This time over I shifted from an inheritance-heavy design to a more modular aggregation-based approach, utilizing objects like Folders and Save Files for a more maintainable design.

The move to aggregation presented most advantages, but I stumbled across a challenge in managing the Asset Library and Save File. In order to offer manual loading options to the Library client, I considered various solutions:

1. Allowing clients to directly manipulate the `Save File` for simplicity, albeit with potential robustness trade-offs.
2. Implementing a new `library.load()` function that recalls the `Save_File.load()`. Though redundant, it allowed for customization of the `library.load()` function.
3. Using delegation to forward the `Save_File.load()` method's interface.
4. Ultimately, I automated data saving and loading, ensuring a seamless user experience without manual intervention.

### Autosave Decorator for Enhanced Code Redability
The autosave decorator was a valuable addition to the API, enhancing code maintainability by simplifying identification of methods that manipulate the metafile. It streamlined internal logic, resulting in reduced code complexity and improved organization. Despite being perceived as "sugar coating," the decorator greatly enhanced code clarity and overall maintainability.

### Nomenclature change from Serializable_File to Save_File
Though this sounds silly, it highlighted an interesting aspect about communications, previously as I talked to my peers about my approach to this assignment I had difficulties the serialization functionality in my project, these difficulties would always end with me exclaiming "_Is a save file! You can save and load stuff like a game..._" to then the entire setup immediately clarified and understood. This situation happened so many times at some point, I realized... if talking in terms of save/load makes this so much easier for people to understand why I am using the serialization deserialization terminology?

### dataclass_json
Using dataclass_json to handle serialization brought some interesting design considerations. In order to use the library I had to wrap my serializable objects into dataclasses decorated by `@dataclass_json`, Admittedly, this approach might seem a bit convoluted, as a more straightforward dictionary inside the manager could have sufficed. However, the benefits of using this design outweighed this drawback. It allowed for easy addition of new fields and structures to my dataclasses, ensuring seamless serialization of new data types. Moreover, it kept a clear separation between what is serializable and what is not within the code, improving code organization. One satisfying aspect is that all fields in these data-containing classes, like LibraryData, are part of its functionality rather than directly manipulating the actual data.

### Missing Archiving Shows and Considerations
I made a deliberate decision not to implement show archiving, as it involves complex considerations. In my setup, archiving a show would require addressing the interdependence of shots, assets, and the entire node system behind them. For instance, if I were to archive a show and all its connected shots, should it also archive shots used by other shows? Recursively archiving a show's contents might lead to unexpected behaviors where other assets' requirements are archived inadvertently. Additionally, unpacking an asset archived by a show raises questions about its impact on the show's setup and other archived assets. These intricacies led me to refrain from implementing show archiving.

However, I did implement asset archiving in an interesting way, which I found to be a more manageable approach.
