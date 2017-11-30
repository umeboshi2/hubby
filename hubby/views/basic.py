import os
from cornice.resource import resource, view

from hubby.database import Department, Person
from hubby.managers.basic import DepartmentManager, PersonManager
from hubby.views.base import BaseManagementResource

APIROOT = '/rest/v0'

rscroot = os.path.join(APIROOT, 'main')
dept_path = os.path.join(rscroot, 'department')
person_path = os.path.join(rscroot, 'person')

@resource(collection_path=dept_path,
          path=os.path.join(dept_path, '{id}'))
class MainDepartmentResource(BaseManagementResource):
    mgrclass = DepartmentManager
    def collection_post(self):
        request = self.request
        db = request.db

@resource(collection_path=person_path,
          path=os.path.join(person_path, '{id}'))
class MainPersonResource(BaseManagementResource):
    mgrclass = PersonManager
    def collection_post(self):
        request = self.request
        db = request.db




    
