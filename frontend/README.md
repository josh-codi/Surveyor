# Surveyor

This program provides a UI for an SA to setup surveys for SPs.

## PROBLEM DESCRIPTION

1. Develop a React.js (SPA-Single Page Application) web application that allows a Survey Admin-SA to create surveys for other users (Survey participant-SP) to complete.
    Use either Python flask framework as your backend.

        Note. Use the "Direct `<script>` Include" approach when developing the SPA. (See <https://reactjs.org/docs/add-react-to-a-website.html#step-2-add-the-script-tags>)

        Each survey should have a name(that is unique), creation and update timestamps. Each Survey will have at least one field under it, which will be rendered as input fields to the SP.

        For a given survey, each field added should have a name/label and an attribute indicating whether the SP is required to provide an input (in other words, fields that can not be skipped)

        The application should allow for the following types of fields with their corresponding constraints and attributes.

        a. Text field (max character length)

        b. Number field (maximum value, minimum value)

        c. Single-select choice field  (options)

2. The application should have the following pages

    a. Survey create/edit page for SA

    b. Survey listings page for SA

    c. Survey instance page for SP to complete and submit

    d. Survey data tabulation page for SA to view all SP submissions.

3. Each SP survey instance submission should have a submission timestamp. Survey submissions must all be validated based on each field's attributes/constraints set by the SA at the time of creation.

4. For each survey the SA should be able to get and share a publicly accessible url (Survey link, SL). SLs will be the SP’s means of accessing survey instances for completion.

5. Implement a basic login for accessing the SA features of the application. A root user account (username:'master', password:'keypass') should be pre-created/pre-loaded when the app is run. SP is not required to login.

6. Include automated tests for the features you develop.

7. Use Sqlite database as your database backend

8. Use pip and virtualenv to manage your python dependencies

9. Use git to manage and track your progress.

10. Send us the url to your github repo for the project when you are done.

11. Do well to submit a near production-ready/complete project.

12. Send us the url to your github repo (PRIVATE) for the project when you are done.

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

#### Production deployment

See recommendations at <https://www.toptal.com/flask/flask-production-recipes>

#### Project Structure

Partly based on <https://github.com/pallets/flask/tree/main/examples/tutorial>

## TODO

- Implement change of password
- Automated testing
