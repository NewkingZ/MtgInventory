# This library interacts with the collections in the storage folder

import os.path
import os
import csv
import pandas as pd
import modules.mtgcards as mtgcards

ALL = "Library"
STORAGE = "./storage/"
CARDMID = "MultiverseID"
CARDNAME = "CardName"
CARDSET = "SetName"
CARDTYPE = "Type"
CARDRARITY = "Rarity"
CARDCID = "ColorID"
CARDCOST = "Cost"
CARDQTY = "Qty"
CARDFOILS = "FoilQty"


# Make a local collection
def make_collection(name):
    # Check to see if the file name has any problems, if its already there, etc...
    if not name.isalnum():
        print("name is not alphanumeric")
        return

    # Make the file
    if name[:-4] != ".csv" or name[:-4] != ".CSV":
        name = name + ".csv"

    with open(STORAGE + name, "w+") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([CARDMID, CARDNAME, CARDSET, CARDRARITY, CARDTYPE, CARDCID, CARDCOST,
                         CARDFOILS, CARDQTY])


def remove_collection(name):
    # TODO: Check to see if the file exists
    if name[:-4] != ".csv" or name[:-4] != ".CSV":
        name = name + ".csv"
    os.remove(STORAGE + name)


# Get a list of current collections
def get_collections():
    # Make sure the storage folder is available
    if not os.path.isdir(STORAGE):
        os.mkdir(STORAGE, 0o755)

    # List out contents of storage
    collections = []
    for coll in os.listdir(STORAGE):
        collections.append(coll[:-4])
    return collections


def import_card_list(card_list_file, collection):
    try:
        print("Importing " + card_list_file + " into " + collection)
        # Open files with csv reader
        import_list = pd.read_csv(card_list_file, sep=',')
        collection_list = pd.read_csv(STORAGE + collection + ".csv", sep=',')

        for card_index in import_list.index:
            if import_list["Foil"][card_index]:
                foil = 1
            else:
                foil = 0
            res = collection_list[collection_list["MultiverseID"] == import_list["Multiverse ID"][card_index]]
            if res.empty:
                print("Card " + import_list["Card Name"][card_index] + " Not found, adding to list")

                fetch_res = mtgcards.fetch_by_id(import_list["Multiverse ID"][card_index])
                collection_list = collection_list.append({
                    "MultiverseID": import_list["Multiverse ID"][card_index],
                    CARDNAME: import_list["Card Name"][card_index],
                    CARDSET: fetch_res.set,
                    CARDRARITY: fetch_res.rarity,
                    CARDTYPE: fetch_res.type,
                    CARDCID: mtgcards.stringify_color_id(fetch_res),
                    CARDCOST: fetch_res.mana_cost.replace('{', '').replace('}', ''),
                    CARDFOILS: foil,
                    CARDQTY: "1",
                    }, ignore_index=True)
            else:
                print("card found already in collection, increasing count")
                collection_list.loc[res.index[0], "Qty"] = int(collection_list.loc[res.index[0], "Qty"]) + 1
                if foil:
                    collection_list.loc[res.index[0], "FoilQty"] = int(collection_list.loc[res.index[0], "FoilQty"]) + 1

        print(collection_list)
        collection_list.to_csv(STORAGE + collection + ".csv", index=True)
        return True

    except:
        return False


def collection_size(collection_name):
    collection_list = pd.read_csv(STORAGE + collection_name + ".csv", sep=',')
    return len(collection_list.index)


def collection_get_cards(collection_name, starting_index, count):
    collection_list = pd.read_csv(STORAGE + collection_name + ".csv", sep=',')
    # Case 1: Starting index is too high; Return nothing:
    if len(collection_list.index) < starting_index:
        return None
    # Case 2: Starting index is fine, but count goes higher than the number of cards available; return what it can
    if len(collection_list.index) < starting_index + count:
        return collection_list
    # Case 3: The starting index is fine and adding the count is still within the boundaries; return chunk
    return collection_list[starting_index:starting_index+count]
