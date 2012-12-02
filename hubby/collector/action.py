import re

from base import BaseCollector

ACTION_DATA_IDENTIFIERS = dict(file_id='_hypFile',
                        ftype='_lblType',
                        mover='_hypMover',
                        seconder='_hypSeconder',
                        result='_lblResult',
                        agenda_note='_lblAgendaNote',
                        minutes_note='_lblMinutesNote',
                        action='_lblAction',
                        action_text='_lblActionText'
                        )


class ActionCollector(BaseCollector):
    def _get_votes(self, page):
        tables = page.find_all('table', class_='rgMasterTable')
        if len(tables) != 1:
            msg = "Problem with determining master table len(tables) = %d"
            raise RuntimeError , msg % len(tables)
        table = tables.pop()
        items = []
        for row in table.find_all('tr')[1:]:
            person, vote = row.find_all('td')
            name = person.text.strip()
            link = person.a['href']
            vote = vote.text.strip()
            items.append((name, link, vote))
        return items
            
    def _get_action(self, page):
        markers = ACTION_DATA_IDENTIFIERS
        item_keys = markers.keys()
        item = {}.fromkeys(item_keys)
        for key in item_keys:
            exp = re.compile('.+%s$' % markers[key])
            tags = page.find_all('span', id=exp)
            if not tags:
                tags = page.find_all('a', id=exp)
            if not tags:
                print "NO TAGS FOR", key
                continue
            if len(tags) > 1:
                print "len(%s) == %d" % (key, len(tags))
            tag = tags[0]
            if markers[key].startswith('_lbl'):
                # just text with lbl
                item[key] = tag.text.strip()
            elif markers[key].startswith('_hyp'):
                name = tag.text.strip()
                link = tag['href']
                item[key] = (name, link)
            else:
                item[key] = tag
        item['votes'] = self._get_votes(page)
        return item

    def collect(self):
        self.retrieve_page(self.url)
        self.action = self._get_action(self.soup)
        self.result = self.action
        
                
if __name__ == "__main__":
    url = 'http://hattiesburg.legistar.com/HistoryDetail.aspx?ID=6153632&GUID=1376DD13-58E1-443A-9A2E-F218CE70C4B6'
    ac = ActionCollector()
    ac.retrieve_page(url)
    i = ac._get_action(ac.soup)
    