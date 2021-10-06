# Surveyor

This program provides a UI for an SA to setup surveys for SPs.



## Development Setup

### Backend

Per the requirement, this project uses Python Flask as a backend server.
Dependencies are managed with pip, preferably in a virtual environment.

From a terminal, run:

    ```sh
    cd ./backend
    virtualenv .venv    # create a virtual python environment
    source ./.venv/bin/activate     # activate the virtual environment
    pip install -r ./requirements.txt   # install dependencies
    ```

#### Run in development

    ```sh
    # in an activated virtualenv dir, with all dependencies installed
    python surveyor/app.py 
    ```

### FrontEnd
    It uses babel to convert tha jsx to be displayed on the DOM
    

#### Project Structure

Partly based on <https://github.com/pallets/flask/tree/main/examples/tutorial>

## TODO
-Making SA create surveys
-Making SA review and edit surveys
-Allowing SP to answer surveys
- Implement change of password
- Automated testing
