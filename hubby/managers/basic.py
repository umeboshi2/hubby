import transaction

from hubby.database import Department, Person
from hubby.managers.base import BaseManager

class DepartmentManager(BaseManager):
    def query(self):
        return self.session.query(Department)

    def add(self, id, guid, name):
        with transaction.manager:
            dept = Department(id, guid)
            dept.name = name
            self.session.add(dept)
        return self.session.merge(dept)

    
        

class PersonManager(BaseManager):
    def query(self):
        return self.session.query(Person)

    def add(self, data):
        with transaction.manager:
            p = Person()
            for key, value in data.items():
                setattr(p, key, value)
            self.session.add(p)
        return self.session.merge(p)

    
        
