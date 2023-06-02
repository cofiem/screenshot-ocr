import logging
import pathlib
from datetime import timezone, datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class GoogleSheetsClient:
    """A client that provides access to Google Sheets."""

    def __init__(self, credentials_file: pathlib.Path, token_file: pathlib.Path):
        """Create a new Google Sheets Client instance."""
        self._auth_credentials_file = credentials_file
        self._auth_token_file = token_file

        self._client = None
        self._scopes = [
            # "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/spreadsheets",
        ]

    def _authorise(self):
        """Authorise access to the Google Sheets API."""
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self._auth_token_file.exists():
            logger.info("Using credentials from token.json file.")
            creds = Credentials.from_authorized_user_file(
                str(self._auth_token_file), self._scopes
            )

        # If there are no (valid) credentials available, prompt the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Requesting new credentials.")
                creds.refresh(Request())
            else:
                logger.info("Starting authorisation flow.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self._auth_credentials_file), self._scopes
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            logger.info("Saving credentials to token.json file.")
            self._auth_token_file.write_text(creds.to_json())

        return creds

    def client(self):
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

            self._client = build(*build_args, **params)

            logger.info("Created new client.")
        except HttpError as error:
            logger.error("An error occurred %s", error, exc_info=True)

        return self._client


def update_spreadsheet_cell(
    ss_client: GoogleSheetsClient,
    ss_id: str,
    sheet_name: str,
    col: str,
    row: str,
    value: str,
) -> bool:
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
    # TODO: WrapStrategy WRAP
    request = (
        ss_client.client()
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
    if response.get("spreadsheetId") != ss_id or not all([i == 1 for i in []]):
        logger.warning("Unexpected response '%s'.", response)
    return True


def update_trivia_cell(
    ss_client: GoogleSheetsClient,
    ss_id: str,
    question_number: int,
    value: str,
):
    sheet_name = datetime.now(timezone.utc).strftime("%Y-%m-%d %a")
    col = "B"
    if question_number < 21:
        row = str(question_number + 2)
    else:
        row = str(question_number + 5)

    return update_spreadsheet_cell(ss_client, ss_id, sheet_name, col, row, value)
