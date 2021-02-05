import unittest
from conveyr import Conveyor,__handlers__ ,__handlers_per_concrete__
from .process_interfaces import IHasSurname, IHasName, IHasId,IHasCreationDate,\
    IHasNamePayload,IHasSurnamePayload
from .process_object_classes import Employee, CreateEmployeePayload
import importlib

class ConveyrTest(unittest.TestCase):

    def setUp(self):
        import tests.process_handlers
        __handlers__.clear()
        __handlers_per_concrete__.clear()
        importlib.reload(tests.process_handlers)
         # load and register handlers

    def tearDown(self):
        __handlers__.clear()
        __handlers_per_concrete__.clear()

    def test_1(self):
        conveyr = Conveyor()
        self.assertIsNotNone(conveyr)

    def test_2(self):
        
        conveyr = Conveyor()
        employee = Employee()
        payload = CreateEmployeePayload(name='Bob',surname='Freeman',thumbnail_path='sume_thumbnail_path.jpg')
        conveyr.process(employee,payload)
        self.assertEquals(employee.name,'Bob')
        self.assertEquals(employee.surname,'Freeman')
        self.assertFalse(hasattr(employee,'thumbnail_path'))
        self.assertIsNotNone(employee.id)
        self.assertIsNotNone(employee.created_at)


    def test_static_conveyor(self):
        employee = Employee()
        payload = CreateEmployeePayload(name='Bob',surname='Freeman',thumbnail_path='sume_thumbnail_path.jpg')
        Conveyor.process(employee,payload)
        self.assertEquals(employee.name,'Bob')
        self.assertEquals(employee.surname,'Freeman')
        self.assertFalse(hasattr(employee,'thumbnail_path'))
        self.assertIsNotNone(employee.id)
        self.assertIsNotNone(employee.created_at)


    def test_custom_handlers_manager(self):
        def handler_manager(cls:type):
            print('creating handler {}'.format(cls.__name__))
            return cls()

        conveyr = Conveyor(class_handler_manager=handler_manager)
        employee = Employee()
        payload = CreateEmployeePayload(name='Bob',surname='Freeman',thumbnail_path='sume_thumbnail_path.jpg')
        conveyr.process(employee,payload)
        self.assertEquals(employee.name,'Bob')
        self.assertEquals(employee.surname,'Freeman')
        self.assertFalse(hasattr(employee,'thumbnail_path'))
        self.assertIsNotNone(employee.id)
        self.assertIsNotNone(employee.created_at)


    def test_ordering(self):
        conveyr = Conveyor()
        employee = Employee()
        payload = CreateEmployeePayload(name='Bob',surname='Freeman',surname1='Freeman1',thumbnail_path='sume_thumbnail_path.jpg')
        conveyr.process(employee,payload)
        self.assertEquals(employee.name,'Bob')
        self.assertNotEquals(employee.surname,'Freeman')
        self.assertEquals(employee.surname,'Freeman1')
        self.assertFalse(hasattr(employee,'thumbnail_path'))
        self.assertIsNotNone(employee.id)
        self.assertIsNotNone(employee.created_at)
