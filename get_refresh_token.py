import argparse
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secret_json", help="Path to OAuth client secret JSON")
    args = parser.parse_args()

    flow = InstalledAppFlow.from_client_secrets_file(args.client_secret_json, SCOPES)
    creds = flow.run_local_server(port=0)
    print(creds.refresh_token)


if __name__ == "__main__":
    main()
