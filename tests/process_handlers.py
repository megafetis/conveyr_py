from conveyr import Conveyor
from .process_interfaces import IHasId,IHasName,IHasSurname,IHasCreationDate,IHasNamePayload,IHasSurnamePayload, IHasSurnamePayload1, IHasThumbnailPath, IHasThumbnailPathPayload
import uuid
import datetime



@Conveyor.handler()
class SetNameHandler():
    def process(self,entity:IHasName, payload:IHasNamePayload):
        entity.name = payload.name


@Conveyor.handler(order=1)
def set_surname_handler(entity:IHasSurname,payload:IHasSurnamePayload):
    entity.surname = payload.surname


@Conveyor.handler(order=2)
def set_surname_handler1(entity:IHasSurname,payload:IHasSurnamePayload1):
    if payload.surname1:
        entity.surname = payload.surname1


@Conveyor.handler()
def set_id_handler(entity:IHasId):
    entity.id = uuid.uuid4()


@Conveyor.handler()
def set_creagtion_date_handler(entity:IHasCreationDate):
    entity.created_at = datetime.datetime.now()


@Conveyor.handler()
def set_thumbnail_handler(entity:IHasThumbnailPath,payload:IHasThumbnailPathPayload):
    entity.thumbnail_path = payload.thumbnail_path