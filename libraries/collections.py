# This library interacts with the collections in the storage folder

import os.path
import os
import csv
import pandas as pd
import modules.mtgcards as mtgcards

ALL = "Library"
STORAGE = "./storage/"


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

        writer.writerow(["MultiverseID", "CardName", "SetName", "Rarity", "Type", "ColorID", "Cost", "FoilQty", "Qty"])


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
                    "CardName": import_list["Card Name"][card_index],
                    "SetName": import_list["Set Name"][card_index],
                    "Rarity": fetch_res.rarity,
                    "Type": fetch_res.type,
                    "ColorID": mtgcards.stringify_color_id(fetch_res),
                    "Cost": fetch_res.mana_cost.replace('{', '').replace('}', ''),
                    "FoilQty": foil,
                    "Qty": "1",
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



