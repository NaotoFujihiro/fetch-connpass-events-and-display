#  -*- encoding: utf-8 -*-


def create_folders(keyword, drive_service):
    file_metadata = {
        'name': keyword,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    new_file = drive_service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()
    return new_file.get('id')


def move_files(drive_service, file_id, folder_id):
    # Retrieve the existing parents to remove
    previous_file = drive_service.files().get(fileId=file_id,
                                     fields='parents').execute()
    previous_parents = ",".join(previous_file.get('parents'))

    # Move the file to the new folder
    moved_file = drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()

    return moved_file
