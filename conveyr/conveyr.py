
from typing import Any,Callable,Awaitable
import inspect
__handlers__ = []
__handlers_per_concrete__={}

class Conveyor():
    def __init__(self,class_handler_manager = None):
        self.class_handler_manager = class_handler_manager or (lambda cls: cls() )

    class_handler_manager=None

    async def process(self, entity:object, payload:object=None,group:str=None)->Awaitable[dict]:
        resp_dict = {}
        for handler in Conveyor.find_handlers(entity,payload,group):
            resp = (self.class_handler_manager(handler["handler"]).process if handler["isclass"] else handler["handler"])(entity,payload) if \
                 handler["payload_type"] else \
                      (self.class_handler_manager(handler["handler"]).process if handler["isclass"] else handler["handler"])(entity)

            resp_dict[handler["handler"].__name__] = await resp if resp and inspect.isawaitable(resp) else resp
        return resp_dict
            

    @staticmethod
    def register_handler(handler,group:str=None,order = 0,entity_type:type=None,payload_type:type=None):
        handler_func = None
        is_class = False
        if not inspect.isfunction(handler):
            if(hasattr( handler, 'process' ) and callable( handler.process )):
                handler_func = handler.process
                is_class=True
            else:
                raise ValueError("Handler must be a function or a class that contains 'process' method. {function}".format(function = handler))
        else:
            handler_func=handler
        sign = inspect.signature(handler_func)
        items = list(sign.parameters)
        
        if is_class:
            items.remove(items[0])
        params_len = items.__len__()

        if params_len<1:
            raise ValueError("Handler process method must contains minimum 1 argument: entity object, payload object (optional). Handler: {function}".format(function = handler))

        entity_type = entity_type or sign.parameters.get(items[0]).annotation if sign.parameters.get(items[0]).annotation != sign.parameters.get(items[0]).empty else None

        if not entity_type:
            raise ValueError("Type of entity in handler method must be specified. handler: {function}".format(function = handler))

        payload_type = sign.parameters.get(items[1]).annotation if params_len > 1 and sign.parameters.get(items[1]).annotation != sign.parameters.get(items[1]).empty else None

        if params_len>1 and not payload_type:
            raise ValueError("If your handler has payload, his type must be specified. Handler: {function}, payload: {payload}".format(function = handler,payload=payload_type))

        if not any(x["handler"]==handler and x["entity_type"]==entity_type and x["payload_type"]==payload_type and x["group"]==group for x in __handlers__):
            __handlers__.append({"handler":handler,"iscoroutine":inspect.iscoroutinefunction(handler),"isclass":inspect.isclass(handler),"entity_type":entity_type,"payload_type":payload_type,"group":group,"order":order})



    @staticmethod
    def handler(group:str=None,order = 0,entity_type:type=None,payload_type:type=None):
        def decorator_func(handler):
            Conveyor.register_handler(handler=handler,group=group,order=order,entity_type=entity_type,payload_type=payload_type)
            return handler
        return decorator_func


    @staticmethod
    def find_handlers(entity:object, payload:object=None,group:str=None):
        key = '{entity}_{payload}_{group}'.format(entity=entity.__class__.__name__,payload=payload.__class__.__name__ if payload else '',group=group if group else '')

        if not __handlers_per_concrete__.get(key):

            handlers = []

            for value in __handlers__:
                
                if value["group"]==group and \
                     (entity.__class__==value["entity_type"] or value["entity_type"]==Any or issubclass(entity.__class__,value["entity_type"])) and \
                        (payload.__class__== value["payload_type"] or issubclass(payload.__class__,value["payload_type"]) if payload and value["payload_type"] else not value["payload_type"]):
                    handlers.append(value)

            handlers.sort(key=lambda x:x["order"])
            __handlers_per_concrete__[key] = handlers

        return __handlers_per_concrete__[key]
