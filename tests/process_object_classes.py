from .process_interfaces import IHasId,IHasName,IHasSurname,IHasCreationDate,IHasNamePayload,IHasSurnamePayload, IHasSurnamePayload1, IHasThumbnailPathPayload

class Employee(IHasId,IHasName,IHasSurname,IHasCreationDate):
    def __init__(self):
        pass

class CreateEmployeePayload(IHasNamePayload,IHasSurnamePayload,IHasSurnamePayload1,IHasThumbnailPathPayload):
    def __init__(self,name:str,surname:str,surname1:str = None,thumbnail_path:str=None):
        self.name = name
        self.surname = surname
        self.thumbnail_path = thumbnail_path
        self.surname1 = surname1

