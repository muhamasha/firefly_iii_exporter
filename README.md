# Firefly III Exporter

This repo includes a script that exports all transactions from Firefly III to a **CSV** file.

## Usage

1. Clone this repo
2. Install the dependencies using poetry (make sure you have poetry installed)

    ```bash
    poetry lock && poetry install --no-root
    ```
3. Run the script

    ```bash
    poetry run python export.py
    ```

## Configuration

The script uses the following environment variables:

- `FIREFLY_III_BASE_URL`: The base URL of your Firefly III instance
- `FIREFLY_III_API_TOKEN`: The API token of your Firefly III instance

Both can be set in a `.env` file in the root of the project.

### Export duration

The start and end date of the export can be configured in the script itself using `start_date` and `end_date` variables.
