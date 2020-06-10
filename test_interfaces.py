
class IEntity():
    id=None

class IHasNameEntity():
    name = None

class IHasSurnameEntity():
    surname = None

class IHasDesctiptionEntity():
    description = None

class IHasAgeEntity():
    age=0


class INamePayload:
    pass

class ISurnamePayload:
    pass

class IDescriptionPayload:
    pass

class IHasAgePayload():
    age=0

class Entity1(IEntity,IHasNameEntity,IHasSurnameEntity):
   name=None

class Entity2(IEntity,IHasNameEntity,IHasSurnameEntity,IHasDesctiptionEntity):
   pass

class Entity3(IEntity,IHasNameEntity,IHasSurnameEntity,IHasDesctiptionEntity,IHasAgeEntity):
   pass

class Payload1(INamePayload,ISurnamePayload):
    def __init__(self,name,surname,description=None):
        self.name = name
        self.surname = surname
        self.description = description


class Payload2(INamePayload,ISurnamePayload,IDescriptionPayload,IHasAgePayload):
    def __init__(self,name,surname,description,age=0):
        self.name = name
        self.surname = surname
        self.description = description
        self.age = age