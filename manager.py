from worker.map import Map

from dataclasses import dataclass, field
from typing import List
import pickle
import numpy as np

@dataclass
class Map_Infor:
    img_id: int = 0
    map: List[List[List[List]]] = field(default_factory = lambda: [[[[], []] for _ in range(16)] for _ in range(16)])
    chars: List[List[int]] = field(default_factory = lambda: [])

class Manager:
    def __init__(self) -> None:
        self.map = Map()

    def run(self, cam: str, results: list) -> None:
        while True:
            try:
                self.map.Load_Map(cam)
                break
            except:
                temp = Map_Infor()
                with open(f"./infor/map/{cam}.pkl", 'wb') as file:
                    pickle.dump(temp, file)
        try:
            self.map.Run(results)
            self.map.Save_Map()
        except:
            pass