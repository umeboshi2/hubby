class BaseView(object):
    def __init__(self, request):
        self.request = request
        self.response = None
        self.data = {}
    
    def __call__(self):
        if self.response is not None:
            return self.response
        else:
            return self.data


    def get_app_settings(self):
        return self.request.registry.settings


class _BaseResource(object):
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession

    def get_app_settings(self):
        return self.request.registry.settings
    

class BaseResource(_BaseResource):
    def __init__(self, request, context=None):
        super(BaseResource, self).__init__(request)
        if not hasattr(self, 'dbmodel'):
            msg = "need to set dbmodel property before __init__"
            raise RuntimeError(msg)
        
    def _query(self):
        return self.db.query(self.dbmodel)

    def _get(self, id):
        return self._query().get(id)
    
    def get(self):
        id = int(self.request.matchdict['id'])
        return self._get(id).serialize()
    
class BaseManagementResource(_BaseResource):
    def __init__(self, request, context=None):
        super(BaseManagementResource, self).__init__(request)
        if not hasattr(self, 'mgrclass'):
            msg = "need to set mgrclass property before __init__"
            raise RuntimeError(msg)
        self.mgr = self.mgrclass(self.request.dbsession)

    def get(self):
        id = int(self.request.matchdict['id'])
        return self.mgr.get(id).serialize()
    
    def collection_get(self):
        # FIXME: use offset, limit, and pass filters
        objects = self.mgr.all()
        return dict(data=[o.serialize() for o in objects])
