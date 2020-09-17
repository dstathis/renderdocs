#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
import subprocess

from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/drive.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1jwFlPG_q5lr80NYI19L_3mErAv4Yk2-g6uzK113Qiks'

docdir = Path('docs')

def get_doc(service, doc_id):
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=doc_id).execute()

    fname = f'{document["title"]}.md'.replace(' ', '_')
    contents = document['body']['content']
    text = []
    for elt in contents:
        if 'paragraph' in elt:
            text_elements = elt['paragraph']['elements']
            for text_element in text_elements:
                chars = text_element.get('textRun')
                if chars:
                    text.append(chars['content'])
    with (docdir / fname).open('w') as f:
        f.write('\n'.join(text))
    return fname


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v2', credentials=creds)

    docdir.mkdir(exist_ok=True)
    with Path('id.txt').open() as f:
        folder_id = f.read().strip()
    items = drive_service.children().list(folderId=folder_id).execute()['items']
    with open('home.md', 'w') as f:
        for doc in items:
            fname = get_doc(docs_service, doc['id'])
            f.write(f'[{fname}](docs/{fname})  \n')
    subprocess.run(['grip', '-b', 'home.md'])


if __name__ == '__main__':
    main()
