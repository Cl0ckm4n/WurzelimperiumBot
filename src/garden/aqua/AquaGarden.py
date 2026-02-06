#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.garden.Garden import Garden
from src.garden.aqua.Http import Http
from src.logger.Logger import Logger
from src.core.User import User
from src.product.Products import OLD_ROOT, DUCKWEED, GREAT_DIVING_BEATLE

AREA1 = [83,84,85,100,101,102,117,118,119,134,135,136,151,152,153,168,169,170,183,184,185,186,187,200,201,202,203,204] # Quest >= 10
AREA2 = [9,10,11,12,13,14,15,16,17,26,27,28,29,30,31,32,33,34,48,49,50,51] # Quest >= 35
AREA3 = [1,2,3,4,5,6,7,8,18,19,20,21,22,23,24,25,35,36,37,38,52,53,54,55] # Quest >= 50
AREA4 = [137,138,154,155,171,172,173,174,175,176,177,178,179,188,189,190,191,192,193,194,195,196] # Quest >= 60
class AquaGarden(Garden):
    def __init__(self):
        Garden.__init__(self, 101)

        self.__httpAqua = Http()
        self.__setInnerFields()
        self.__setOuterFields()
        self.__set_fields_available()
        self._PLANT_PER_REQUEST = 11

    def __setInnerFields(self, distance=2):
        """defines the fieldID's of the inner watergarden planting area"""
        #BG- """Задава fieldID-тата на полетата във вътрешната област за засаждане във водната градина."""

        self._INNER_FIELDS = []
        for i in range(distance, self._LEN_Y-distance):
            self._INNER_FIELDS.extend(range(i * self._LEN_X + distance + 1, (i + 1) * self._LEN_X - distance + 1))

    def __setOuterFields(self):
        """defines the fieldID's of the outer watergarden planting area"""
        #BG- """Задава fieldID-тата на полетата във външната област за засаждане във водната градина."""

        temp_fields = list(range(1, self._MAX_FIELDS+1))
        self._OUTER_FIELDS = [x for x in temp_fields if x not in self._INNER_FIELDS]

    def __set_fields_available(self):
        self.__fields_available = list(range(1,205))
        aqua_quest = User().get_aquagarden_quest()
        if aqua_quest < 10:
            self.__fields_available = [item for item in self.__fields_available if item not in AREA1]
        if aqua_quest < 35:
            self.__fields_available = [item for item in self.__fields_available if item not in AREA2]
        if aqua_quest < 50:
            self.__fields_available = [item for item in self.__fields_available if item not in AREA3]
        if aqua_quest < 60:
            self.__fields_available = [item for item in self.__fields_available if item not in AREA4]

    def _isPlantGrowableOnField(self, fieldID, emptyFields, fieldsToPlant, edge, sx):
        """Prüft anhand mehrerer Kriterien, ob ein Anpflanzen möglich ist."""
        #BG- """Проверява чрез няколко критерия дали е възможно засаждане."""

        if not (fieldID in self.__fields_available): return False

        # Betrachtetes Feld darf nicht besetzt sein
        #BG- Полето, което се разглежда, не трябва да е заето

        if not (fieldID in emptyFields): return False

        #Randpflanze im Wassergarten
        #BG- # Растение на ръба във водната градина

        if edge == 1:
            if not [x for x in fieldsToPlant if x in self._OUTER_FIELDS] == fieldsToPlant: return False

        #Wasserpflanzen im Wassergarten
        #BG- Водни растения във водната градина

        if edge == 0:
            if not [x for x in fieldsToPlant if x in self._INNER_FIELDS] == fieldsToPlant: return False


        # Anpflanzen darf nicht außerhalb des Gartens erfolgen
        # Dabei reicht die Betrachtung in x-Richtung, da hier ein
        # "Zeilenumbruch" stattfindet. Die y-Richtung ist durch die
        # Abfrage abgedeckt, ob alle benötigten Felder frei sind.
        # Felder außerhalb (in y-Richtung) des Gartens sind nicht leer,
        # da sie nicht existieren.

        if not ((self._MAX_FIELDS - fieldID)%self._LEN_X >= sx - 1): return False
        fieldsToPlantSet = set(fieldsToPlant)
        emptyFieldsSet = set(emptyFields)

        # Alle benötigten Felder der Pflanze müssen leer sein
        #BG- # Всички необходими полета за растението трябва да бъдат празни

        if not (fieldsToPlantSet.issubset(emptyFieldsSet)): return False
        return True

    def getEmptyAquaFields(self):
        """Gibt alle leeren Felder des Gartens zurück."""
        #BG- Връща всички празни полета на градината.
        return self.__httpAqua.get_empty_fields()

    def water(self) -> bool:
        plants = self.__httpAqua.get_plants_to_water()
        if plants is None:
            return False
        nPlants = len(plants['fieldID'])
        if nPlants and self._user.has_watering_gnome_helper():
            if not self.__httpAqua.water_all_plants():
                return False
        else:
            for i in range(0, nPlants):
                sFields = self._getAllFieldIDsFromFieldIDAndSizeAsString(plants['fieldID'][i], plants['sx'][i], plants['sy'][i])
                if sFields is None:
                    return False
                if not self.__httpAqua.water_plants(sFields):
                    return False
        Logger().info(f'Im Wassergarten wurden {nPlants} Pflanzen gegossen.')
        #BG- Във водната градина бяха поляти {nPlants} растения.
        return True

    def harvest(self) -> bool:
        """Erntet alles im Wassergarten."""
        #BG- Събира всичко във водната градина.
        return self.__httpAqua.harvest()

    def grow(self, plantID, sx, sy, edge, amount):
        """Grows a watergarden plant of any size and type."""
        #BG- """Отглежда водно растение във водната градина с всякакъв размер и вид."""

        planted = 0
        emptyFields = self.getEmptyAquaFields()
        if emptyFields is None:
            return None

        to_plant = {}
        try:
            for field in range(1, self._MAX_FIELDS + 1):
                if planted == amount: break

                fieldsToPlant = self._getAllFieldIDsFromFieldIDAndSizeAsIntList(field, sx, sy)

                if (self._isPlantGrowableOnField(field, emptyFields, fieldsToPlant, edge, sx)):
                    to_plant.update({field: None}) #collect all plants for a request

                    # Nach dem Anbau belegte Felder aus der Liste der leeren Felder loeschen
                    #BG- След отглеждането, изтрийте заетите полета от списъка на празните полета
                    fieldsToPlantSet = set(fieldsToPlant)
                    emptyFieldsSet = set(emptyFields)
                    tmpSet = emptyFieldsSet - fieldsToPlantSet
                    emptyFields = list(tmpSet)

                if len(to_plant) == self._PLANT_PER_REQUEST or len(to_plant) + planted == amount \
                or (field == self._MAX_FIELDS and len(to_plant) > 0):
                    if self.__httpAqua.grow(to_plant, plantID) is None:
                        return None
                    planted += len(to_plant)
                    to_plant = {}
            return planted
        finally:
            Logger().print(f'Im Wassergarten wurden {planted} Pflanzen gepflanzt.')
            #BG- Във водната градина са засадени {planted} растения.
            if emptyFields:
                Logger().print(f'Im Wassergarten sind noch {len(emptyFields)} leere Felder vorhanden.')
                #BG- Във водната градина все още има {len(emptyFields)} празни полета.

    def __get_weed_fields(self):
        """Returns all weed fields in the garden."""
        #BG- """Връща всички полета с плевели в градината."""
        return self.__httpAqua.get_weed_fields() or {}
    
    def remove_weeds(self) -> bool:
        """
        Entfernt alles Unkraut, Steine und Maulwürfe, wenn ausreichend Geld vorhanden ist.
        """
        #BG- Премахва всички плевели, камъни и кърлежи, ако има достатъчно пари.

        # Load details for all fields of this garden
        garden = self.__httpAqua.init_garden()
        if garden is None:
            return False
        garden = garden.get('garden')

        money = User().get_bar()
        all_weeds_removed = True
        weedFieldsAqua = self.__get_weed_fields()
        freeFields = []
        for fieldID in weedFieldsAqua:
            # Check if user has enough money to pay for the removal
            field_info = garden[str(fieldID)]
            weed_type = field_info[0]
            cost_map = {OLD_ROOT: 100, DUCKWEED: 10, GREAT_DIVING_BEATLE: 500}
            cost_for_removal = cost_map.get(weed_type)

            if cost_for_removal > money:
                Logger().debug('Not enough money to remove the weeds')
                all_weeds_removed = False
                continue

            money -= cost_for_removal

            # Remove weed on field
            result = self.__httpAqua.remove_weed_on_field(fieldID)
            if result is None:
                Logger().print_error(f'Feld {fieldID} im Aquagarten {self._id} konnte nicht von Unkraut befreit werden!')
                #BG- f'Полето {fieldID} в Аква-градината {self._id} не може да бъде освободено от плевели!')
                return False

            if result == 1:
                Logger().info(f'Feld {fieldID} im Aquagarten {self._id} wurde von Unkraut befreit!')
                #BG- Полето {fieldID} в Аква-градината {self._id} беше освободено от плевели!
                freeFields.append(fieldID)
            else:
                Logger().print_error(f'Feld {fieldID} im Aquagarten {self._id} konnte nicht von Unkraut befreit werden!')
                    #BG- Полето {fieldID} в Аква-градината {self._id} не може да бъде освободено от плевели!

        Logger().print(f'Im Aquagarten {self._id} wurden {len(freeFields)} Felder von Unkraut befreit.')
        if all_weeds_removed:
            Logger().print(f'Im Aquagarten {self._id} wurden ALLE Felder von Unkraut befreit.')
        #BG- В Аква-градината {self._id} бяха освободени от плевели {len(freeFields)} полета.

        return True
