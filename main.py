from pathlib import Path
import datetime
import re
import win32com.client  #pip install pywin32
from ocrparse import convert_pdf_to_searchable_pdf
import os
OUTPUT = "Output"
# Create output folder
output_dir = Path.cwd() / OUTPUT
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Connect to folder
inbox = outlook.Folders("davidlu31415@outlook.com").Folders("Inbox")
proceesed_folder = outlook.Folders("davidlu31415@outlook.com").Folders("Processed")
# inbox = outlook.GetDefaultFolder(6)
# https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
# DeletedItems=3, Outbox=4, SentMail=5, Inbox=6, Drafts=16, FolderJunk=23

# Get messages
messages = inbox.Items
to_be_moved = []
for message in messages:
    subject = message.Subject
    body = message.body
    attachments = message.Attachments
    if not len(attachments):
       continue
    # Create separate folder for each message, exclude special characters and timestampe
    target_folder = output_dir
    target_folder.mkdir(parents=True, exist_ok=True)

    # Write body to text file
    try: 
        body_text = str(body)
    except:
        continue
    # Path(target_folder / "EMAIL_BODY.txt").write_text(str(body_text))
    flag = False
    # Save attachments and exclude special
    for attachment in attachments:
        filename = re.sub('[^0-9a-zA-Z\.]+', '', attachment.FileName)
        if(filename[-3:] != "pdf"):
            continue
        attachment.SaveAsFile(target_folder / filename)
        flag = True
    if flag:
        to_be_moved.append(message)
print(to_be_moved)

for i in to_be_moved:
    i.Move(proceesed_folder)

files = os.listdir(OUTPUT)
for f in files:
    input_path = os.path.join(OUTPUT, f)
    convert_pdf_to_searchable_pdf(input_path, OUTPUT + "/" + f[:-4] + "_processed.pdf")
    os.remove(input_path)
    