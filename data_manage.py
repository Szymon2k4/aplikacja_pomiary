import csv
import os




def save_file():
    pass

def data_man(file_name, headlines, data_table):
    #tab: [nazwa, typ_bez, ipz_zab, prad_zw_zab, ipz_obl, obl_pr_zwarc, ocena, id, datetime.date(yyyy, mm, dd)]
    print(data_table)

    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headlines)
        writer.writerow(data_table)

    


def remove_data_using_id(data):
    file_name = 'pomiary/name.csv'
    print('do usuniecia', data)

    removed_id = set()
    if isinstance(data, list):
        for d in data:
            removed_id.add(d)
    else:
        removed_id.add(data)


    with open(file_name, "r", newline="") as f:
        reader = list(csv.reader(f))  # Konwersja do listy
    
    print('rem_id', removed_id)
    for i, ms in enumerate(reader):
        print(ms[7])
        if ms[7] in removed_id:
            reader[i][9] = 'del'

    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(reader)
            

        


def read(file_name):
    with open(file_name, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            print(r)

def load_measuremenst():
    file_name = 'nazwy_pomiarow.csv'

    with open(file_name, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)



def is_file_name_exist(file_name, data):
    # zmienic na os.fileexist, przeszukiwnaie folderu
    with open(file_name, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    print(reader)
    read = list()

    for d in reader:
        try:
            if d[0] == data:
                return True
        except IndexError:
            continue
    return False

    



    
    
