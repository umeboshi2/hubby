import os
from cornice.resource import resource, view

from hubby.database import Department, Person
from hubby.managers.main import MeetingManager
from hubby.views.base import BaseManagementResource
from hubby.views.base import BaseView

APIROOT = '/rest/v0'

rscroot = os.path.join(APIROOT, 'main')
dept_path = os.path.join(rscroot, 'department')
person_path = os.path.join(rscroot, 'person')
meeting_path = os.path.join(rscroot, 'meeting')

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
            items = []
            for i in m.items:
                idata = i.serialize()
                if len(i.attachments):
                    attachments = []
                    for a in i.attachments:
                        attachments.append(a.serialize())
                    idata['attachments'] = attachments
                if len(i.actions):
                    actions = []
                    for a in i.actions:
                        actions.append(a.serialize())
                    idata['actions'] = actions
                items.append(idata)
            mdata['items'] = items
        return dict(data=mdata, result='success')




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
        
        
    def get_ranged_meetings(self):
        start, end = self._get_start_end_from_request()
        meetings = self.mgr.get_ranged_meetings(start, end,
                                                timestamps=True)
        mlist = list()
        for m in meetings:
            #mdata = dict(id=m.id, title=m.title,
            #             url='/hello/%d' % m.id)
            #del mdata['url']
            #mdata = dict(id=m.id, title=m.title)
            mdata = m.serialize()
            del mdata['rss']
            home = self.request.route_url('home')
            print "HOME", home
            #mdata['url'] = m.id
            #data['url'] = 'http://localhost:6543/#hubby/viewmeeting/%d' % m.id
            #mdata['url'] = 'http://localhost:6543/foo'
            
            mlist.append(mdata)
        self.response = mlist
        
