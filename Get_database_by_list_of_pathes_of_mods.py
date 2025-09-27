import re
from collections import defaultdict
from pathlib import Path

from Levenshtein import ratio  # Библиотека python-Levenshtein
from lxml import etree
from printy import printy

from GlobFunc import error_handler, no_comment_parser
from Settings_module import SVV as S


class MultiIndexDict:
    """
    MultiIndexDict {'name': str, 'packageid': str, 'path': Path}
            db.find(name='Vanilla Factions Expanded - Ancients')
            db.find(packageId='Neronix17.OuterRim.GalacticDiversity')
            db.partial_find(name='combat exten')
            db.fuzzy_find(name='ce')
    """
    def __init__(self, case_insensitive_fields=None, fuzzy_fields=None, synonyms=None, partial_match_fields=None):
        self.records = []
        self.indices = {}
        self.case_insensitive_fields = {f.lower() for f in case_insensitive_fields} if case_insensitive_fields else set()
        self.fuzzy_fields = {f.lower() for f in fuzzy_fields} if fuzzy_fields else set()
        self.partial_match_fields = {f.lower() for f in partial_match_fields} if partial_match_fields else set()

        # Словарь синонимов
        self.synonyms = synonyms or {}
        self.synonym_map = {}
        for canonical, syn_list in self.synonyms.items():
            norm_canonical = self._normalize_value("name", canonical, fuzzy=False)
            for syn in syn_list:
                norm_syn = self._normalize_value("name", syn, fuzzy=False)
                self.synonym_map[norm_syn] = norm_canonical

    def _normalize_field(self, field):
        return field.lower()

    def _normalize_value(self, field, value, fuzzy=False):
        if not isinstance(value, str):
            return value

        field_lower = field.lower()

        # Case-insensitive
        if field_lower in self.case_insensitive_fields:
            value = value.lower()

        # Fuzzy-нормализация
        if fuzzy and field_lower in self.fuzzy_fields:
            value = re.sub(r'[^\w\s]', '', value)
            value = re.sub(r'\s+', ' ', value).strip()

        return value

    def _expand_with_synonyms(self, field, value):
        if field.lower() != "name":
            return [value]

        normalized = self._normalize_value(field, value, fuzzy=False)
        results = {normalized}

        if normalized in self.synonym_map:
            results.add(self.synonym_map[normalized])

        if normalized in self.synonyms:
            for syn in self.synonyms[normalized]:
                results.add(self._normalize_value(field, syn, fuzzy=False))

        return list(results)

    def add(self, record):
        idx = len(self.records)
        self.records.append(record)

        for field, value in record.items():
            norm_field = self._normalize_field(field)

            variants = set()
            variants.add(value)

            if field.lower() in self.case_insensitive_fields:
                variants.add(self._normalize_value(field, value))

            if field.lower() in self.fuzzy_fields:
                variants.add(self._normalize_value(field, value, fuzzy=True))

            for variant in variants:
                self._add_to_index(idx, norm_field, variant)

    def _add_to_index(self, idx, field, value):
        if field not in self.indices:
            self.indices[field] = defaultdict(list)

        self.indices[field][value].append(idx)

    def find(self, fuzzy_search=False, **conditions):
        if not conditions:
            return None

        matched_indices = None
        for field, value in conditions.items():
            norm_field = self._normalize_field(field)

            search_values = set()
            for v in [value] + self._expand_with_synonyms(field, value):
                search_values.add(v)

                if field.lower() in self.case_insensitive_fields:
                    search_values.add(self._normalize_value(field, v))

                if fuzzy_search and field.lower() in self.fuzzy_fields:
                    search_values.add(self._normalize_value(field, v, fuzzy=True))

            field_indices = set()
            for search_value in search_values:
                if norm_field in self.indices and search_value in self.indices[norm_field]:
                    field_indices.update(self.indices[norm_field][search_value])

            if not field_indices:
                return []

            if matched_indices is None:
                matched_indices = field_indices
            else:
                matched_indices &= field_indices

        return [self.records[i] for i in matched_indices] if matched_indices is not None else []

    def fuzzy_find(self, **conditions):
        return self.find(fuzzy_search=True, **conditions)

    def partial_find(self, min_score=0.85, **conditions):
        """Поиск по частичному совпадению с использованием алгоритма Левенштейна"""
        if not conditions:
            return None
        results = []
        for record in self.records:
            match = True
            total_score = 0
            fields_count = 0

            for field, query in conditions.items():
                if field not in record:
                    match = False
                    break

                # Нормализуем значение в записи
                record_value = str(record[field])
                norm_record_value = self._normalize_value(field, record_value, fuzzy=True)

                # Нормализуем запрос
                norm_query = self._normalize_value(field, query, fuzzy=True)

                # Рассчитываем схожесть
                score = ratio(norm_record_value, norm_query)
                total_score += score
                fields_count += 1

                # Проверяем минимальный порог
                if field.lower() in self.partial_match_fields:
                    if score < min_score:
                        match = False
                        break
                else:
                    if norm_query not in norm_record_value:
                        match = False
                        break

            if match:
                # Добавляем запись с оценкой схожести
                results.append({
                    "record": record,
                    "score": total_score / fields_count if fields_count > 0 else 0
                })

        # Сортируем по убыванию схожести
        results.sort(key=lambda x: x["score"], reverse=True)
        return [item["record"] for item in results]

    def __getitem__(self, key):
        return self.find(**key)

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)



def searching_all_packageIds(mod_path_list, database):
    processed_idx = 0
    for mp in mod_path_list:
        if mp is None:
            continue

        for f in Path(mp).iterdir():
            printy(f"\r\tProcessed: {processed_idx} Elements", 'b>', end='')
            processed_idx += 1
            if not f.is_dir():
                continue
            try:
                p = f / 'About' / 'About.xml'
                res = parse_xml_file(p)
                if res is not None:
                    database.add(res)
            except Exception as ex:
                print("Bad reading", f, str(ex))




def parse_xml_file(file: Path):

    try:
        tree = etree.parse(file, parser=no_comment_parser)
        root = tree.getroot()

        name_value = "NOT FOUND"
        package_id_value = "NOT FOUND"

        # Перебираем только прямых потомков корневого элемента
        for child in root:
            # print(child.tag, type(child.tag))
            tag_lower = child.tag.lower()

            if tag_lower == "name":
                name_value = child.text
            elif tag_lower == "packageid":
                package_id_value = child.text

            # Прерываем цикл если оба значения найдены
            if name_value != "NOT FOUND" and package_id_value != "NOT FOUND":
                break

        results = {'name': name_value, 'packageid': package_id_value, 'path': file.parent.parent}
        return results

    except Exception as e:
        print(f"Ошибка в файле {file}: {str(e)}")





def get_packageID_names_pathes_database(list_of_folders_to_search_mods:list[Path]):
    """
    MultiIndexDict {'name': str, 'packageid': str, 'path': Path}
            db.find(name='Vanilla Factions Expanded - Ancients')
            db.find(packageId='Neronix17.OuterRim.GalacticDiversity')
            db.partial_find(name='combat exten')
            db.fuzzy_find(name='ce')
    """
    synonyms = {
        'core': ['rimworld - core',],
        "royalty": ["rimworld - royality", "royalty [official dlc]"],
        "ideology": ["rimworld - ideology", 'ideology [official dlc]'],
        "biotech": ["rimworld - biotech", 'biotech [official dlc]'],
        "anomaly": ["rimworld - anomaly", 'anomaly [official dlc]'],

        "combat extended": ["ce"],
        "vanilla factions expanded deserters": ["deserters"],

    }
    @error_handler(error_text="No Data folder")
    def add_data_pathes_in_database(dbb):
        rimworld_data_path = S.Path_to_Data

        aa = [
            ('core',    'Ludeon.RimWorld',          Path(rimworld_data_path) / 'Core'),
            ('Royalty', 'Ludeon.RimWorld.Royalty',  Path(rimworld_data_path) / 'Royalty'),
            ('Ideology','Ludeon.RimWorld.Ideology', Path(rimworld_data_path) / 'Ideology'),
            ('Biotech', 'Ludeon.RimWorld.Biotech',  Path(rimworld_data_path) / 'Biotech'),
            ('Anomaly', 'Ludeon.RimWorld.Anomaly',  Path(rimworld_data_path) / 'Anomaly'),
            ('Odyssey', 'Ludeon.RimWorld.Odyssey',  Path(rimworld_data_path) / 'Odyssey'),
        ]
        for a in aa:
            name, iid, path = a
            if path.exists():
                dbb.add({'name': name, 'packageid': iid, 'path': path})

    db = MultiIndexDict(case_insensitive_fields=["name", "packageId"], fuzzy_fields=["name"], partial_match_fields=["name"], synonyms=synonyms)

    add_data_pathes_in_database(db)

    searching_all_packageIds(list_of_folders_to_search_mods, db)
    printy('\n')
    # a1 = db.find(name='Vanilla Factions Expanded - Ancients')
    # a1 = db.find(packageId='Neronix17.OuterRim.GalacticDiversity')
    # a1 = db.partial_find(name='combat exten')
    # a1 = db.fuzzy_find(name='ce')
    # pprint(a1)

    return db



