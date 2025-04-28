from client import FMCClient

client = FMCClient.from_credentials(
    host="x.x.x.x",
    port=51443,
    username="admin",
    password="Admin123",
    domain_name="Global",
)
DYN_OBJ_NAME = 'mydynamic'
MY_IP = '172.19.1.1'
all_dynamic_objects = client.dynamic_objects.get_all()
for dyn_obj in all_dynamic_objects.items:
    if dyn_obj.name == DYN_OBJ_NAME:
        client.dynamic_objects.remove_mapping([MY_IP], dyn_obj.id)
        exit()
print('Dynamic object not found!')