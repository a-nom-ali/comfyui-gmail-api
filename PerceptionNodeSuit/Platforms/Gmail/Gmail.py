import os.path
import re
from datetime import datetime
import dateutil.parser as parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from py_linq import Enumerable
from email.message import EmailMessage
import os
import base64
from typing import List
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
import numpy as np

import folder_paths


class GmailException(Exception):
    """gmail base exception class"""


class NoEmailFound(GmailException):
    """no email found"""


class Gmail:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def __init__(self):
        self.service = None
        self.creds = None

    def authorize(self, credentials_path=None, no_service=False):
        if self.service is None:
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            token_filename = "{}.token.json".format(self.SCOPES[0].split("/")[-1])
            if os.path.exists(token_filename):
                self.creds = Credentials.from_authorized_user_file(token_filename, self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not credentials_path:
                        credentials_path = "{}/credentials.json".format(os.path.dirname(__file__))
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(token_filename, "w") as token:
                    token.write(self.creds.to_json())

            # Call the Gmail API
            if not no_service:
                self.service = build("gmail", "v1", credentials=self.creds)

            return token_filename

    def authorize_with_token(self, token_path):
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                    self.service = build("gmail", "v1", credentials=self.creds)
                    return True
            else:
                self.service = build("gmail", "v1", credentials=self.creds)
                return True
        return False

    def search_emails(self, query_string: str, label_ids: List = None):
        try:
            message_list_response = self.service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string
            ).execute()

            message_items = message_list_response.get('messages')
            next_page_token = message_list_response.get('nextPageToken')

            while next_page_token:
                message_list_response = self.service.users().messages().list(
                    userId='me',
                    labelIds=label_ids,
                    q=query_string,
                    pageToken=next_page_token
                ).execute()

                message_items.extend(message_list_response.get('messages'))
                next_page_token = message_list_response.get('nextPageToken')
            return message_items
        except Exception as e:
            raise NoEmailFound(f'No emails returned:{e}')

    def threads(self, query_string: str, label_ids: List = None):
        """Load threads matching query_string and label_ids)
        Return: None
        """

        try:
            # pylint: disable=maybe-no-member
            # pylint: disable:R1710
            return (
                self.service.users().threads().list(
                    userId="me",
                    labelIds=label_ids,
                    q=query_string
                ).execute().get("threads", [])
            )

        except HttpError as error:
            print(f"An error occurred: {error}")

    def thread(self, thread_id):
        """Load threads matching query_string and label_ids)
        Return: None
        """

        try:
            # pylint: disable=maybe-no-member
            # pylint: disable:R1710
            return (
                self.service.users().threads().get(
                    userId="me",
                    id=thread_id)
                .execute()["messages"]
            )

        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_file_data(self, message_id, attachment_id):
        response = self.service.users().messages().attachments().get(
            userId='me',
            messageId=message_id,
            id=attachment_id
        ).execute()

        file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
        return file_data

    def get_message_detail(self, message_id, msg_format='metadata', metadata_headers: List = None):
        message_detail = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format=msg_format,
            metadataHeaders=metadata_headers
        ).execute()
        return message_detail

    def get_messages(self, q):
        results = (self.service
                   .users()
                   .messages()
                   .list(userId="me", q=q)
                   .execute())

        return results.get('messages')

    def send_message(self, message_body: str, subject: str, to_email: str, from_email: str, attachments: list = None,
                     thread_id: str = None, extra_pnginfo=None):
        """Create and send an email message
        Print the returned  message id
        Returns: Message object, including message id    """

        try:
            message = EmailMessage()

            message.set_content(message_body)

            filename_prefix = "gmail_attachment_"
            output_dir = folder_paths.get_output_directory()

            # I added this part
            if attachments and len(attachments) > 0:
                counter = 0
                for attachment in attachments:
                    is_path = True
                    if not isinstance(attachment, str):
                        is_path = False
                        full_output_folder, filename, counter, sub_folder, filename_prefix = (
                            folder_paths.get_save_image_path(
                                filename_prefix,
                                output_dir,
                                attachment.shape[1],
                                attachment.shape[0]))

                        i = 255. * attachment.cpu().numpy()
                        content = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                        metadata = PngInfo()
                        if extra_pnginfo is not None:
                            for x in extra_pnginfo:
                                metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                        filename = f"{filename_prefix}{counter:05}_.png"
                        attachment = os.path.join(full_output_folder, filename)
                        content.save(attachment, pnginfo=metadata, compress_level=4)

                    with open(attachment, 'rb') as content_file:
                        content = content_file.read()
                        message.add_attachment(content, maintype='application', subtype=(attachment.split('.')[1]),
                                               filename=attachment.split("/")[-1].split("\\")[-1])

                    if not is_path:
                        os.remove(attachment)

                    counter += 1

            message['To'] = to_email
            message['From'] = from_email
            create_message = {
            }
            if thread_id is not None:
                thread = self.thread(thread_id)
                thread_subject = self.get_thread_subject(thread)
                message['Subject'] = thread_subject if thread_subject is not None else subject
                create_message["threadId"] = thread_id
            else:
                message['Subject'] = subject  # "{}{}".format("" if not thread_id else "Re ", subject)

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message['raw'] = encoded_message

            # pylint: disable=E1101
            send_message = (self.service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        return send_message

    def mark_messages_as_read(self, message_id):
        self.update_message_labels(message_id, [], ['UNREAD'])

    def update_message_labels(self, message_id, add_label_ids=[], remove_label_ids=[]):
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={
                'addLabelIds': add_label_ids,
                'removeLabelIds': remove_label_ids
            }
        ).execute()

    def get_thread_subject(self, messages):
        if len(messages) == 0:
            return None
        else:
            msg = messages[0]
            txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']

            subject = Enumerable(headers) \
                .where(lambda x: x["name"] == 'Subject') \
                .first()["value"]

            return subject

    def process_messages(self, messages, strip_history=True):
        results = []
        for msg in messages:
            body_message = ""
            attachments = []
            # Get the message from its id
            # print(msg)
            txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']

            from_email = Enumerable(headers) \
                .where(lambda x: x["name"] == 'From') \
                .first()["value"]

            to_email = Enumerable(headers) \
                .where(lambda x: x["name"] == 'To') \
                .first()["value"]

            subject = Enumerable(headers) \
                .where(lambda x: x["name"] == 'Subject') \
                .first()["value"]

            if subject.find(":") > -1:
                # continue
                subject = subject.replace(":", "")

            clean_subject = subject.replace(" ", "")

            email_date_str = (Enumerable(headers).where(lambda x: x["name"] == 'Date').first()["value"])

            email_date = parser.parse(email_date_str)

            parts = payload.get('parts')

            if parts:
                for part in parts:
                    # Check if part is an attachment
                    if part['filename']:
                        filename = part['filename']
                        if not (filename.lower().endswith("jpg") or filename.lower().endswith("png")):
                            continue
                        filepath = f"./input/4DID/{clean_subject}"
                        filename = f"{filepath}/{filename}"

                        if not os.path.exists(filepath):
                            os.makedirs(filepath)

                        attachment_id = part['body']['attachmentId']

                        attachments.append({
                            "filename": filename,
                            "image": self.get_file_data(msg['id'], attachment_id)
                        })
                        #
                        # # Save attachment to local disk
                        # with open(filename, 'wb') as f:
                        #     f.write(file_data)

                        print(f'Saved attachment: {filename}')
                    else:
                        if part["mimeType"] in ["text/plain", "text/html"]:
                            body_message += base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        # body = part.get("body")
                        # data = body.get("data")
                        # mime_type = part.get("mimeType")
                        #
                        # if mime_type == 'multipart/alternative':
                        #     subparts = part.get('parts')
                        #     for p in subparts:
                        #         body = p.get("body")
                        #         data = body.get("data")
                        #         mime_type = p.get("mimeType")
                        #         if mime_type == 'text/plain':
                        #             body_message += data
                        #         elif mime_type == 'text/html':
                        #             body_message += data
                        #
                        #
                        # # without attachment
                        # elif mime_type == 'text/plain':
                        #     body_message += base64.urlsafe_b64decode(data)
                        # elif mime_type == 'text/html':
                        #     body_message += base64.urlsafe_b64decode(data)

            body = txt["snippet"] if not body_message or body_message == "" else body_message
            results.append({
                "to": to_email,
                "from": from_email,
                "subject": subject,
                "date": email_date,
                "body": re.split(r'\s*On [\w, :]+<[\w_\-]+@[\w_\-]+\.[\w_\-]+> wrote:\s*', body)[0],
                "attachments": attachments,
                "message": msg
            })

            # print(from_email)
            # print(subject)
            # print(email_date)
            # print(body)
            # print(attachments)

        return results

