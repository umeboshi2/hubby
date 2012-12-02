from base import BaseCollector

from people import PeopleCollector
from departments import DeptCollector
from meeting import MeetingCollector
from item import ItemCollector
from action import ActionCollector

class _MainCollector(PeopleCollector, DeptCollector,
                     MeetingCollector, ItemCollector,
                     ActionCollector):
    pass


class MainCollector(_MainCollector):
    def __init__(self):
        _MainCollector.__init__(self)
        self.dept_url = 'http://hattiesburg.legistar.com/Departments.aspx'
        self.people_url = 'http://hattiesburg.legistar.com/People.aspx'
        self.url_prefix = 'http://hattiesburg.legistar.com/'
        self._map = dict(people=PeopleCollector,
                         dept=DeptCollector,
                         meeting=MeetingCollector,
                         item=ItemCollector,
                         action=ActionCollector)

    def collect(self, ctype):
        self._map[ctype].collect(self)
        

if __name__ == "__main__":
    murl = 'http://hattiesburg.legistar.com/MeetingDetail.aspx?From=RSS&ID=209045&GUID=6F113835-7E47-432D-B3BA-2140AC586A6C'
    iurl = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1221728&GUID=9CC815CB-387A-42BF-B442-B80F953CB51E&Options=&Search='
    iurl2 = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1195041&GUID=8DB3A9EB-569C-477C-9F3B-B04EFD8AA955&Options=&Search='
    aurl = 'http://hattiesburg.legistar.com/HistoryDetail.aspx?ID=6153632&GUID=1376DD13-58E1-443A-9A2E-F218CE70C4B6'
    mc = MainCollector()
    mc.set_url(murl)
    
