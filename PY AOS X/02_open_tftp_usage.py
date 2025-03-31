
from 02_open_tftp import tftp_receive, tftp_send

switch_ip = "10.241.63.200"
username = "admin"
password = "@dm1.n"
remote_file = "config_with_stp_update"
local_file = "new_config.cfg"

tftp_receive(switch_ip, username, password, remote_file, local_file)

file_to_upload = "new_config.cfg"
file_to_download = "startup-config"

tftp_send(switch_ip, username, password, file_to_upload, file_to_download)