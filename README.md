# conveyr_py
Conveyor pipline handling library for python 3.5 and later

```py
from conveyr import Conveyor
import asyncio
def name_handler():
  pass


conveyor = Conveyor()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(conveyor.process(entity,payload)) 
loop.close()
```
in python 3.6 and later:
```py
 results = asyncio.run(conveyor.process(entity,payload))
```
```py
print(results) // dict of results if handlers returns anything
print(entity.id)
print(entity.name)
print(entity.surname)
print(entity.age)
```
