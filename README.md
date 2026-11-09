## nrl-lib

- **Description**

    - nrl-lib is a Python client for the Nominal Response Library (NRL)
      v2 web service run by EarthScope. The NRL is a curated collection of
      instrument responses for seismic sensors and dataloggers. nrl-lib
      lets you query it from Python instead of building service URLs by
      hand, and can be added to any Python project as a dependency.
    - Supported queries:
        - `catalog`: list instrument types, manufacturers, models and
          configuration parameters available in the NRL (XML, JSON or text)
        - `combine`: build complete sensor + datalogger instrument
          responses, optionally stamped with network/station/location/
          channel epoch information, as StationXML, StationXML-Response or
          RESP (single files or .zip bundles)
        - `prefix-lookup`: retrieve the table of instrument-configuration
          prefixes with their names and associated logic-tree questions
    - Responses can be returned in memory or written to files, with
      configurable error handling and logging.
    - The distribution is named `nrl-lib`; the Python package is imported
      as `nrl`.


  - **Installation**
    - From conda-forge
    ```
    conda install -c conda-forge nrl-lib
    ```
    - From source, to install and test the library
    ```
    - conda create -n testNRL python=3.11
    - conda activate testNRL
    - pip install -e .
    ```

- **Usage**
    - This library doesn't provide any CLI or GUI accessibility. It can be 
      imported in any Python project as an independent library.
    ```
    from nrl.NRLQuery import NRLQuery
    ```
    - To have a quick start on how to use the library, please check the scripts exist in the `test_script` folder.


- **License**: GNU General Public License v3 (GPLv3)
