from tinydb import TinyDB, Query

from api.models import Thought, Plex
from api.models.plex.plex_state_diff import PlexStateDiff
from api.models.interfaces.thoughtsstorage import ThoughtsStorage


class TinyStorage(ThoughtsStorage):
    def __init__(self):
        self.db = TinyDB("db.json")

    def get_thought(self, id):
        query = Query()
        result = self.db.search(query.id == id)
        if len(result) > 0:
            return Thought(result[0])
        return None

s = TinyStorage()
p = Plex(s)
d = PlexStateDiff()

lo = p.activate(s.get_thought(2))
ln = p.activate(s.get_thought(4))

d.diff(lo, ln)

print(lo.get_state())
#t1 = Thought({"id":1,"title":"first", "links":[]})
#t2 = Thought({"id":2,"title":"second", "links":[]})
#t3 = Thought({"id":3,"title":"third", "links":[]})
#t4 = Thought({"id":4,"title":"fourth", "links":[]})

#p.link_thoughts(t1, t2, "parent->child")
#p.link_thoughts(t1, t4, "parent->child")
#p.link_thoughts(t2, t3, "parent->child")

#1->2->3
#1->4
#

#p.link_thoughts(t1)

#db.insert(t1.to_dictionary())
#db.insert(t2.to_dictionary())
#db.insert(t3.to_dictionary())
#db.insert(t4.to_dictionary())