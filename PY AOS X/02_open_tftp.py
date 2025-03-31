##open tftp

import tftpy
import io     #will handle file transfer between local host and switch

#This function requires you to know the destination filepath and the local filepaths
def tftp_receive(switch_ip, username, password, remote_file, local_file):

    try:
        tftp_auth = f"{username}@{password}"

        client = tftpy.TftpClient(switch_ip, 69) #Creates a tftp client, over UDP 69

        context = tftpy.TftpContext(client, tftpy.TftpSession(client, tftp_auth))

        client.download(remote_file, local_file, context=context) #Retrieves the file

        print(f"File '{remote_file}' successfully transfered to '{local_file}'.")

    except tftpy.TftpException as e:
        print(f"TFTP Error: {e}") 
    except Exception as e:
        print(f"Some error occurred: {e}")

def tftp_send(switch_ip, username, password, local_file, remote_file):
  try:
    tftp_auth = f"{username}@{password}"

    client = tftpy.TftpClient(switch_ip, 69)

    context = tftpy.TftpContext(client, tftpy.TftpSession(client, tftp_auth))

    client.upload(local_file, remote_file, context=context)

    print(f"File '{local_file}' successfully uploaded to '{remote_file}'.")

  except tftpy.TftpException as e:
    print(f"TFTP Error: {e}")
  except Exception as e:
    print(f"Some error occurred: {e}")

