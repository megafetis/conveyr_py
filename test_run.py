from typing import Any,Type
from conveyr import Conveyor
from test_interfaces import IEntity,Entity1,Entity2,Entity3,INamePayload,ISurnamePayload,Payload1,Payload2
import asyncio
from test_handlers import entity_name_handler,entity_surname_handler


conveyor = Conveyor()


entity = Entity3()

payload = Payload2("evgeniy","fetisov","descr",20)
loop = asyncio.get_event_loop()
results = loop.run_until_complete(conveyor.process(entity,payload))

assert hasattr(entity,'description'), "Should contain description"

print(results)

print(entity.id)
print(entity.name)
print(entity.surname)
print(entity.age)



loop.close()