import os
import time as tim
import dropbox
import re
import hashlib
import yaml
from valve.rcon import RCON


# access token for dropbox
access_token = 'access_token_dropbox'

# minecraft rcon password
rcon_address = ("127.0.0.1", 25575)
rcon_password = "Rcon-Password"

# Itemadder part
ItemsAdder = 'C:\\Users\\kig\\Desktop\\server-1.18.2\\server-test\\plugins\\ItemsAdder'
ItemsAdder_zip = ItemsAdder+'\\data\\resource_pack\\pack.zip'
ItemsAdder_yml = ItemsAdder+'\\config.yml'

delay_uploadfile = 10 # delay upload file to dropbox

# rcon run command
def reload_ia():
    with RCON(rcon_address, rcon_password) as rcon:
        rcon.execute("iareload", block=False, timeout=10)
        tim.sleep(5)
        rcon.execute("iatexture all", block=False)

# get hash file from computer
def hash_file(filename):

    h = hashlib.sha1()

    with open(filename, 'rb') as file:

        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()


def upload_file(file_from, file_to):
    dbx = dropbox.Dropbox(access_token)
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to)
    link = dbx.sharing_create_shared_link(file_to)
    url = link.url
    dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
    return dl_url


def edit_yml_file(name):
    with open(ItemsAdder_yml) as f:
        list_doc = yaml.full_load(f)
    list_doc["resource-pack"]['hosting']['external-host']['url'] = name
    with open(ItemsAdder_yml, "w") as f:
        yaml.dump(list_doc, f)

# main function
times = ''
while True:
    time = os.path.getmtime(ItemsAdder_zip)
    if time != times:
        tim.sleep(delay_uploadfile)
        times = os.path.getmtime(ItemsAdder_zip)
        file_to = '/'+hash_file(ItemsAdder_zip)+'.zip'
        url_d = upload_file(ItemsAdder_zip, file_to)
        # print(url_d)
        edit_yml_file(url_d)
        reload_ia()
        print("New File : "+str(time))
    tim.sleep(1)
