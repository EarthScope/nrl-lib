## nrl-lib

- **Description**

    - nrl-lib provides access to the NRL v2 web service. This library
      can be added to any Python project as a new dependency and provide
      different functionalities to communicate with the remote server.
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
