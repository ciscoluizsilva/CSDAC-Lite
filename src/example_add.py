from client import FMCClient
from client.dynamic_objects.models import NewDynamicObject

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
        client.dynamic_objects.add_mapping([MY_IP], dyn_obj.id)
        exit()
print('Dynamic object not found')
dyn_obj = client.dynamic_objects.create(
    NewDynamicObject(
        name=DYN_OBJ_NAME,
        description="My dynamic object"
    )
)
client.dynamic_objects.add_mapping([MY_IP], dyn_obj.id)