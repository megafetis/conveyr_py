from test_interfaces import IEntity,IHasNameEntity,IHasAgeEntity,IHasAgePayload,IHasSurnameEntity,IHasDesctiptionEntity,INamePayload,ISurnamePayload,IDescriptionPayload
from conveyr import Conveyor
import uuid
@Conveyor.handler(order=5)
async def entity_name_handler(entity:IHasNameEntity,payload:INamePayload):
    entity.name = payload.name

@Conveyor.handler(order=4)
def entity_surname_handler(entity:IHasSurnameEntity,payload:ISurnamePayload):
    entity.surname = payload.surname

@Conveyor.handler(order=3)
def entity_id_handler(entity:IEntity):
    entity.id = uuid.uuid4().hex

@Conveyor.handler(order=2)
def entity_description_handler(entity:IHasDesctiptionEntity,payload:IDescriptionPayload):
    entity.description = payload.description

@Conveyor.handler(order=1)
class PersonAgeHandler:
    def process(self,entity:IHasAgeEntity,payload:IHasAgePayload):
        entity.age = payload.age

