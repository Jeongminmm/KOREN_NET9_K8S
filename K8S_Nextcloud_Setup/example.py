#pip install pyncclient
import nextcloud_client

id = 'nextcloud_ID'
pw = 'nextcloud_PW'

nc = nextcloud_client.Client('http://IP:31014')

nc.login(id, pw)

#nc.mkdir('testdir')

nc.put_file('testdir/test1.png', 'test.png')

link_info = nc.share_file_with_link('test/test.png') +"/preview"

print(link_info)