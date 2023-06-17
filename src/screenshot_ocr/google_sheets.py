"""Google Sheets helpers."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from google.auth.transport import requests
from google.oauth2 import credentials
from google_auth_oauthlib import flow
from googleapiclient import discovery, errors

if TYPE_CHECKING:
    import pathlib

logger = logging.getLogger(__name__)


class GoogleSheetsHelper:
    """A helper that provides access to Google Sheets."""

    def __init__(
        self,
        credentials_file: pathlib.Path,
        token_file: pathlib.Path,
    ) -> None:
        """Create a new Google Sheets Helper instance.

        Args:
            credentials_file: Path to the Google OAuth app client secrets file.
            token_file: Path to the current Google OAuth token file.
        """
        if not credentials_file:
            msg = "Must provide path to credentials file."
            raise ValueError(msg)
        if not credentials_file.exists():
            msg = f"Credentials file is missing '{credentials_file}'."
            raise FileNotFoundError(msg)
        self._auth_credentials_file = credentials_file

        if not token_file:
            msg = "Must provide path to token file."
            raise ValueError(msg)
        if not token_file.parent.exists():
            msg = f"Directory containing token file is missing '{token_file.parent}'."
            raise FileNotFoundError(msg)

        self._auth_token_file = token_file

        self._client = None
        self._scopes = [
            # "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/spreadsheets",
        ]

    def _authorise(self) -> credentials.Credentials | None:
        """Authorise access to the Google Sheets API."""
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self._auth_token_file.exists():
            logger.info("Using credentials from token.json file.")
            creds = credentials.Credentials.from_authorized_user_file(
                str(self._auth_token_file),
                self._scopes,
            )

        # If there are no (valid) credentials available, prompt the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Requesting new credentials.")
                creds.refresh(requests.Request())
            else:
                logger.info("Starting authorisation flow.")
                flow_result = flow.InstalledAppFlow.from_client_secrets_file(
                    str(self._auth_credentials_file),
                    self._scopes,
                )
                creds = flow_result.run_local_server(port=0)

            # Save the credentials for the next run
            logger.info("Saving credentials to token.json file.")
            self._auth_token_file.write_text(creds.to_json())

        return creds

    def client(self) -> discovery.Resource | None:
        """Get the client."""
        if self._client:
            logger.debug("Using existing client.")
            return self._client

        creds = self._authorise()

        try:
            # NOTE: Tried to use the MemoryCache,
            # but the cache does not seem to be used?
            # https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841
            build_args = ["sheets", "v4"]
            params = {"cache_discovery": False, "credentials": creds}

            self._client = discovery.build(*build_args, **params)

            logger.info("Created new client.")
        except errors.HttpError as error:
            logger.exception("Error: %s - %s", error.__class__.__name__, str(error))

        return self._client

    def update_spreadsheet_cell(
        self,
        ss_id: str,
        sheet_name: str,
        col: str,
        row: str,
        value: str,
    ) -> bool:
        """Update the given cell in the spreadsheet to value.

        Update the spreadsheet identified by `ss_id`, changing sheet `sheet_name`,
        column `col`, row `row` to `value`.

        Args:
            ss_id: The Google Spreadsheet id.
            sheet_name: The name of the sheet.
            col: The column identifier.
            row: The row identifier.
            value: Set the cell to this value.

        Returns:
            True if the update succeeded, otherwise false.
        """
        # https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
        value_input_option = "USER_ENTERED"
        major_dimension = "ROWS"
        range_notation = f"'{sheet_name}'!{col}{row}:{col}{row}"
        body = {
            "range": range_notation,
            "majorDimension": major_dimension,
            "values": [[value]],
        }
        # TODO: consider using WrapStrategy WRAP?
        request = (
            self.client()
            .spreadsheets()
            .values()
            .update(
                spreadsheetId=ss_id,
                range=range_notation,
                valueInputOption=value_input_option,
                body=body,
                includeValuesInResponse=False,
            )
        )

        logger.info('Updating spreadsheet cell "%s".', range_notation)

        response = request.execute()
        if response.get("spreadsheetId") != ss_id:
            logger.warning("Unexpected response '%s'.", response)
        return True
