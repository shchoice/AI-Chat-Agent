from fastapi import APIRouter
from typing import List

class RouterRegistry:
    def __init__(self):
        self._routers: List[APIRouter] = []

    def register(self, router: APIRouter):
        self._routers.append(router)

    def get_registered_routers(self) -> List[APIRouter]:
        return self._routers
        