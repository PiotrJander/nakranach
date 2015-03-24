from .pubs import PubList, PubView, TapList, TapChangeList
from .changes import ChangesView
from .auth import FacebookAuthenticate, Logout, Login, Register
from .location import NearestPubsView, NearestActivitiesView

__all__ = [
    # pub views
    'PubList', 'PubView', 'TapList', 'TapChangeList',
    
    # changes views
    'ChangesView',

    # auth views
    'Login', 'FacebookAuthenticate', 'Logout', 'Register',

    # location views
    'NearestPubsView', 'NearestActivitiesView'
]