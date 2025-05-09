from worker.character import Character
from worker.checker import Checker
from worker.map import Map

from dataclasses import dataclass, field
from typing import List

@dataclass
class Map_Infor:
  img_id: int = 0
  map: List[List[List[List]]] = field(default_factory=lambda: [[[[], []] for _ in range(16)] for _ in range(16)])
  chars: List[List[int]] = field(default_factory = [[]])

class Manager:
    def __init__(self) -> None:
        self.path = "./map_cam/"
        self.map = Map(Checker(), Character())

    def run(self, cam: str, result: list) -> None:
        while True:
            try:
                self.map.Load_Map(self.path + cam)
                break
            except:
                temp = Map_Infor()
                with open(self.map_path, 'wb') as file:
                    pickle.dump(self.cam, file)
                
        try:
            char_violen = self.map.Run(result)
            self.map.Save_Map