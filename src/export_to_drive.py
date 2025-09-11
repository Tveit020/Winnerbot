from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class GoogleDriveManager:
    def __init__(self, creds_file="mycreds.txt"):
        self.creds_file = creds_file
        self.drive = self._authenticate_drive()

    def _authenticate_drive(self):
        gauth = GoogleAuth()

        # Try to load saved client credentials
        gauth.LoadCredentialsFile(self.creds_file)

        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh if expired
            gauth.Refresh()
        else:
            # Initialize saved creds
            gauth.Authorize()

        # Save the current credentials to a file
        gauth.SaveCredentialsFile(self.creds_file)

        return GoogleDrive(gauth)

    def create_folder(self, folder_name, parent_folder_id=None):
        folder_metadata = {
            "title": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder_id:
            folder_metadata["parents"] = [{"id": parent_folder_id}]

        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()

        print(f"Folder '{folder_name}' created with ID: {folder['id']}")
        return folder["id"]

    def upload_file(
        self, local_file="output.xlsx", base_file="Pick2025.xlsx", folder_id=None
    ):
        # base_file = os.path.basename(local_file)
        # base_file = "Pick2025.xlsx"
        # Search for existing file with the same name in the folder
        query = f"title='{base_file}' and trashed=false"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        file_list = self.drive.ListFile({"q": query}).GetList()

        if file_list:
            # Overwrite the first found file
            gfile = file_list[0]
            gfile.SetContentFile(local_file)
            gfile.Upload()
            print(f"Overwritten existing file '{base_file}' in Google Drive")
            return gfile["id"]
        else:
            # Create new file
            file_metadata = {"title": base_file}
            if folder_id:
                file_metadata["parents"] = [{"id": folder_id}]
            gfile = self.drive.CreateFile(file_metadata)
            gfile.SetContentFile(local_file)
            gfile.Upload()
            print(f"Uploaded new file '{base_file}' to Google Drive")
            return gfile["id"]


if __name__ == "__main__":
    gdrive = GoogleDriveManager()

    # Create a new folder
    # folder_id = gdrive.create_folder("Scores")
    folder_id = "1GZvN3wq27RqxPQc3di0PrHebwOPPoZrY"

    # Upload a file to that folder
    gdrive.upload_file("output/output.xlsx", folder_id=folder_id)
