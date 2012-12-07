import re

from hubby.util import onclick_link

from base import BaseCollector

ITEM_DATA_IDENTIFIERS = dict(file_id='_lblFile2',
                        name='_lblName2',
                        filetype='_lblType2',
                        status='_lblStatus2',
                        introduced='_lblIntroduced2',
                        on_agenda='_lblOnAgenda2',
                        attachments='_lblAttachments2',
                        title='_lblTitle2',
                        passed='_lblPassed2',
                        action_details='_hypDetails'
                        )

class ItemCollector(BaseCollector):
    def _get_item(self, page):
        markers = ITEM_DATA_IDENTIFIERS
        item_keys = markers.keys()
        item = {}.fromkeys(item_keys)
        for key in item_keys:
            #print "trying for key", key
            exp = re.compile('.+%s$' % markers[key])
            tags = page.find_all('span', id=exp)
            if not tags:
                tags = page.find_all('a', id=exp)
            if not tags and key == 'action_details':
                continue
            if len(tags) > 1:
                print "len(%s) == %d" % (key, len(tags))
            if key == 'action_details':
                #item[key] = tags[0]
                a = tags[0]
                item[key] = onclick_link(a['onclick'])
                continue
            if key == 'attachments' and len(tags):
                chunk = tags[0]
                attachments = []
                for anchor in chunk.find_all('a'):
                    name = anchor.text.strip()
                    link = anchor['href']
                    attachments.append((name, link))
                item[key] = attachments
                continue
            if not len(tags) and key == 'attachments':
                continue
            item[key] = tags[0].text.strip()
        return item
    
    def collect(self):
        self.retrieve_page(self.url)
        self.item = self._get_item(self.soup)
        self.result = self.item
        
    
                
if __name__ == "__main__":
    url = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1221728&GUID=9CC815CB-387A-42BF-B442-B80F953CB51E&Options=&Search='
    url = 'http://hattiesburg.legistar.com/LegislationDetail.aspx?ID=1195041&GUID=8DB3A9EB-569C-477C-9F3B-B04EFD8AA955&Options=&Search='
    ic = ItemCollector()
    ic.set_url(url)
    ic.retrieve_page()
    ic.collect()
    i = ic.item
    
