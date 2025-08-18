#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from src.logger.Logger import Logger
from src.note.Http import Http
from src.product.ProductData import ProductData

class NoteSettings(Enum):

    GARDEN_PLANT_1 = "gardenPlant1:"
    GARDEN_PLANT_2 = "gardenPlant2:"
    WATERGARDEN_PLANT_1 = "watergardenPlant1:"
    WATERGARDEN_PLANT_2 = "watergardenPlant2:"
    WATERGARDEN_PLANT_EDGE = "watergardenPlantEdge:"
    BEE_HIVES = "beeHives:"
    IVY_TYPE = "ivy:"
    HERBGARDEN_ACTIVE = "herbgarden:"

class Note:
    """This class handles reading from the user notes"""

    def __init__(self):
        self.__http = Http()
        self.__product_data = ProductData()
        self._garden_plant_1 = None
        self._garden_plant_2 = None
        self._watergarden_plant_1 = None
        self._watergarden_plant_2 = None
        self._watergarden_plant_edge = None
        self._bee_hives = None
        self._ivy = None
        self._herbgarden_active = False

    # MARK: Basic functions

    def get_note(self) -> str:
        return self.__http.get_note() or ''

    # MARK: Extended features
    
    def get_garden_plant_1(self) -> str:
        return self._garden_plant_1
    
    def get_garden_plant_2(self) -> str:
        return self._garden_plant_2
    
    def get_watergarden_plant_1(self) -> str:
        return self._watergarden_plant_1
    
    def get_watergarden_plant_2(self) -> str:
        return self._watergarden_plant_2
    
    def get_watergarden_plant_edge(self) -> str:
        return self._watergarden_plant_edge
    
    def get_bee_hive(self) -> str:
        return self._bee_hives
    
    def get_ivy(self) -> str:
        return self._ivy
    
    def get_herbgarden_active(self) -> bool:
        return self._herbgarden_active

    def __extract_amount(self, line, prefix) -> int:
        min_stock_str = line.replace(prefix, '').strip()
        try:
            return int(min_stock_str)
        except Exception:
            Logger().error(f'Error: "{prefix}" must be an int')
        return 0

    def get_min_stock(self, plant_name = None) -> int:
        note = self.get_note().replace('\r\n', '\n')
        lines = note.split('\n')

        is_plant_given = not plant_name is None
        for line in lines:
            if line.strip() == '':
                continue

            if not is_plant_given and line.startswith('minStock:'):
                return self.__extract_amount(line, 'minStock:')

            if is_plant_given and line.startswith(f'minStock({plant_name}):'):
                return self.__extract_amount(line, f'minStock({plant_name}):')

        # Return default 0 if not found in note
        return 0

    def get_grow_only(self) -> list[str]:
        note = self.get_note().replace('\r\n', '\n')
        lines = note.split('\n')

        for line in lines:
            if line.strip() == '' or not line.startswith('growOnly:'):
                continue

            line = line.replace('growOnly:', '').strip()
            return list(map(str.strip, line.split(',')))

        # Return default [] if not found in note
        return []
    
    def get_bonus_plant_id(self) -> int:
        note = self.get_note().replace('\r\n', '\n')
        lines = note.split('\n')

        for line in lines:
            if line.strip() == '' or not line.startswith('bonusPlant:'):
                continue

            line = line.replace('bonusPlant:', '').strip()
            plant_id = self.__product_data.get_product_by_name(line).get_id()
            return plant_id
        return None
    
    def get_note_settings(self) -> None:
        note = self.get_note().replace('\r\n', '\n')
        lines = note.split('\n')

        for line in lines:
            if line.strip() == '':
                continue
            for setting in (NoteSettings):
                if not line.startswith(setting.value):
                    continue

                line = line.replace(setting.value, '').strip()
                if line.strip() == '':
                    continue
                try:
                    if setting == NoteSettings.IVY_TYPE:
                        self._ivy = line
                        print('➡ src/note/Note.py:128 self._ivy:', self._ivy)
                    if setting == NoteSettings.HERBGARDEN_ACTIVE:
                        print(f"\n\n\n {line}")
                        print(type(line))
                        if line == "1":
                            self._herbgarden_active = True
                    else:
                        plant_name = self.__product_data.get_product_by_name(line).get_name()
                except:
                    self.__log.error(f"Could not find plant: {line}")
                else:

                    if setting == NoteSettings.GARDEN_PLANT_1:
                        self._garden_plant_1 = plant_name
                    if setting == NoteSettings.GARDEN_PLANT_2:
                        self._garden_plant_2 = plant_name
                    if setting == NoteSettings.WATERGARDEN_PLANT_1:
                        self._watergarden_plant_1 = plant_name
                    if setting == NoteSettings.WATERGARDEN_PLANT_2:
                        self._watergarden_plant_2 = plant_name
                    if setting == NoteSettings.WATERGARDEN_PLANT_EDGE:
                        self._watergarden_plant_edge = plant_name
                    if setting == NoteSettings.BEE_HIVES:
                        self._bee_hives = plant_name


    def get_stop_bot(self) -> bool:
        note = self.get_note().replace("\r\n", "\n")
        lines = note.split("\n")
        for line in lines:
            if line.strip() == "":
                continue

            if line.startswith("stopWIB"):
                return True

        # Return default False if not found in note
        return False
