import csv
import os
from  typing import List, Set, Any


MEASUREMENTS_HEADLINES =  ['id', 'measure_name', 'fuse_type', 'measured_ipz', 'calculated_scircut_bo_measure', 'calculated_ipz', 'calculated_scircut_bo_fuse_type', 'grade', 'datetime.date(yyyy, mm, dd)', 'is_deleted']
MEASUREMENTS_FOLDER = 'measurements_data'


def dm_add_measurement(file_name: str, data_table: Set):
    file_path: str = os.path.join(MEASUREMENTS_FOLDER, file_name) 
    file_exists: bool = os.path.isfile(file_path)
    if not file_exists:
        raise FileNotFoundError
    data = [elem for elem in data_table.values()]
    
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def dm_write_measurements(file_name: str, data: List[List[Any]]):
    file_path = os.path.join(MEASUREMENTS_FOLDER, file_name)
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(MEASUREMENTS_HEADLINES)
        writer.writerows(data)


def dm_create_new_measuremets_file(file_name: str):
    file_path: str = os.path.join(MEASUREMENTS_FOLDER, file_name)
    headlines = MEASUREMENTS_HEADLINES
    file_exists: bool = os.path.isfile(file_path)
    if file_exists:
        return 1

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headlines)


def dm_read_measurements(file_name: str, type = 'list', include_removed_data = True):
    file_path = os.path.join(MEASUREMENTS_FOLDER, file_name)
    if not file_path:
        raise NotImplementedError 
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = [elem for elem in reader if elem != [] ][1:]

    if not include_removed_data:  
        data = [elem for elem in data if elem[9] == 'NOT_DELETED']  

    if type == 'list':
        return data
    elif type == 'dict':
        all_data = list()
        i = 0
        while True:
            dict_data = dict()
            try:
                for key, val in zip(MEASUREMENTS_HEADLINES, data[i]):
                    dict_data[key] = val
                all_data.append(dict_data)
                i += 1
            except IndexError:
                break
        return all_data

    else:
        raise ValueError
    
    


def dm_read_all_measurements_file_name():
    try:
        files = os.listdir(MEASUREMENTS_FOLDER)
        file_names_without_extension = [os.path.splitext(file)[0] for file in files if file.endswith('.csv')]
        return file_names_without_extension
    except FileNotFoundError :
        raise FileNotFoundError
    
    



def dm_remove_data_using_id(file_name, id_to_remove):
    file_path: str = os.path.join(MEASUREMENTS_FOLDER, file_name)

    removed_id: Set = set()
    if isinstance(id_to_remove, list):
        for d in id_to_remove:
            removed_id.add(d)
    else:
        removed_id.add(id_to_remove)


    all_data = dm_read_measurements(file_name, include_removed_data=True)
    for i, ms in enumerate(all_data):
        if ms[0] in removed_id:
            all_data[i][9] = 'DELETED'

    dm_write_measurements(file_name, all_data)




def dm_new_measurements_file_and_note(file_name, note):
    FILE = 'file_names_and_initial_notes.csv'
    file_exists: bool = os.path.isfile(FILE)
    if not file_exists:
        #create file
        raise NotImplementedError
    
    data = [file_name, note]
    
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)







    
    
