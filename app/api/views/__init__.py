from .pubs import PubList, PubView, TapList, TapChangeList, WaitingBeerList, ChangeBeerView
from .changes import ChangesView
from .auth import FacebookAuthenticate, Logout, Login, Register
from .location import NearestPubsView, NearestActivitiesView
from .favorites import FavoritesListView, ToggleFavoriteView, FavoriteTapChanges

__all__ = [
    # pub views
    'PubList', 'PubView', 'TapList', 'TapChangeList', 'WaitingBeerList', 'ChangeBeerView',
    
    # changes views
    'ChangesView',

    # auth views
    'Login', 'FacebookAuthenticate', 'Logout', 'Register',

    # location views
    'NearestPubsView', 'NearestActivitiesView',
    
    # favorite views
    'FavoritesListView', 'ToggleFavoriteView', 'FavoriteTapChanges'
]
