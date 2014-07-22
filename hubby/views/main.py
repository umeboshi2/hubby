import os
from cornice.resource import resource, view

from hubby.database import Department, Person
from hubby.managers.main import MeetingManager, ActionManager
from hubby.views.base import BaseManagementResource
from hubby.views.base import BaseView

APIROOT = '/rest/v0'

rscroot = os.path.join(APIROOT, 'main')
dept_path = os.path.join(rscroot, 'department')
person_path = os.path.join(rscroot, 'person')
meeting_path = os.path.join(rscroot, 'meeting')
action_path = os.path.join(rscroot, 'action')

@resource(collection_path=meeting_path,
          path=os.path.join(meeting_path, '{id}'),
          cors_origins=('*',))
class MeetingResource(BaseManagementResource):
    mgrclass = MeetingManager
    def collection_get(self):
        meetings = [m.serialize() for m in self.mgr.all()]
        for m in meetings:
            if 'rss' in m:
                del m['rss']
        return dict(data=meetings, result='success')
    
    def get(self):
        id = int(self.request.matchdict['id'])
        m = self.mgr.get(id)
        if m is None:
            # FIXME
            raise RuntimeError, '404'
        mdata = m.serialize()
        # remove rss object
        del mdata['rss']
        if len(m.meeting_items):
            meeting_items = []
            for mi in m.meeting_items:
                meeting_items.append(mi.serialize())
            mdata['meeting_items'] = meeting_items
        if len(m.items):
            items = dict()
            for i in m.items:
                idata = i.serialize()
                if len(i.attachments):
                    attachments = []
                    for a in i.attachments:
                        atdata = a.serialize()
                        atdata['url'] = a.get_link()
                        attachments.append(atdata)
                    idata['attachments'] = attachments
                if len(i.actions):
                    actions = []
                    for a in i.actions:
                        actions.append(a.serialize())
                    idata['actions'] = actions
                items[i.id] = idata
            mdata['items'] = items
        return dict(data=mdata, result='success')

@resource(collection_path=action_path,
          path=os.path.join(action_path, '{id}'),
          cors_origins=('*',))
class ActionResource(BaseManagementResource):
    mgrclass = ActionManager
    def collection_get(self):
        return dict(data=[], result='notyet')

    def get(self):
        id = int(self.request.matchdict['id'])
        a = self.mgr.get(id)
        if a is None:
            # FIXME
            raise RuntimeError, '404'
        adata = a.serialize()
        return dict(data=adata, result='success')
    
    



# json view for calendar
class MeetingCalendarViewer(BaseView):
    def __init__(self, request):
        super(MeetingCalendarViewer, self).__init__(request)
        self.mgr = MeetingManager(self.request.db)
        self.get_ranged_meetings()
        
        
    def _get_start_end_from_request(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        return start, end
        
    # json responses should not be lists
    # this method is for the fullcalendar
    # widget.
    def get_ranged_meetings(self):
        start, end = self._get_start_end_from_request()
        meetings = self.mgr.get_ranged_meetings(start, end,
                                                timestamps=True)
        mlist = list()
        for m in meetings:
            mdata = m.serialize()
            del mdata['rss']
            mlist.append(mdata)
        headers = [('Access-Control-Allow-Origin', '*')]
        self.request.response.headerlist.extend(headers) 
        self.response = mlist
        
