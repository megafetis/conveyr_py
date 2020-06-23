# conveyr_py
Conveyor pipline handling library for python 3.5 and later

Requirements:
* Python >= 3.5

## Usage:
install [conveyr](https://pypi.org/project/conveyr/):

`pip install conveyr`

```py
from conveyr import Conveyor
import asyncio


#### define interfaces

```py
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
```

#### define payloads

```py
class INamePayload:
    pass

class ISurnamePayload:
    pass

class IDescriptionPayload:
    pass

class IHasAgePayload():
    age=0
```

#### define concrete entity class an dpayload class
```py
class Entity(IEntity,IHasNameEntity,IHasSurnameEntity,IHasDesctiptionEntity,IHasAgeEntity):
   pass

class Payload(INamePayload,ISurnamePayload,IDescriptionPayload,IHasAgePayload):
    def __init__(self,name,surname,description,age=0):
        self.name = name
        self.surname = surname
        self.description = description
        self.age = age
        
```
#### Define handlers per interface

```py
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

#you can define class handler, wich contains `process` method
@Conveyor.handler(order=1)
class PersonAgeHandler:
    def process(self,entity:IHasAgeEntity,payload:IHasAgePayload):
        entity.age = payload.age

```
#### Run conveyor

```py

conveyor = Conveyor()
loop = asyncio.get_event_loop()

entity = Entity()

payload = Payload('evgeniy','fetisov','some description',30)

results = loop.run_until_complete(conveyor.process(entity,payload)) 
loop.close()
```
#in python 3.6 and later: results = asyncio.run(conveyor.process(entity,payload))
```py
print(results) # dict of results if handlers returns anything
print(entity.id) # some guid id
print(entity.name) # 'evgeniy'
print(entity.surname) # 'fetisov'
print(entity.description) #'some description'
print(entity.age) # 30
```

#### advanced

You can group handlers to several 'layers'

and manage handling orders
```py
@Conveyor.handler(order=5,group="aftercommit")
async def some_handler(entity:IHasNameEntity,payload:INamePayload):
    entity.name = payload.name
#...
results = loop.run_until_complete(conveyor.process(entity,payload,"aftercommit")) # handlers with such group only executed

```
If you are using class handlers, its possible to set custom class handler initializer (or dependency injector)

```py
def some_class_handler_manager(cls):
  return cls()

conveyr = Conveyor(class_handler_manager = some_class_handler_manager)

#...
```
