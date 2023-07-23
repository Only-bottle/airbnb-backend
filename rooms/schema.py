import strawberry
from typing import List, Optional
from . import types
from . import queries
from . import mutations
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    all_rooms: List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
    )
    room: Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )


@strawberry.type
class Mutation:
    room: Optional[types.RoomType] = strawberry.mutation(
        resolver=mutations.add_room,
        permission_classes=[OnlyLoggedIn],
    )