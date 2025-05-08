#!/usr/bin/env python3

import argparse
import urllib.request
import os

parser = argparse.ArgumentParser(description="Télécharge et créer le fichier .json pour les données")
parser.add_argument("lien", help="lien du fichier")
parser.add_argument("destination", help="destination du fichier")
args = parser.parse_args()

def download_file(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"File downloaded successfully to {destination}")
        
    except Exception as e:
        print(f"Failed to download file. Error: {e}")

def delete_first_line(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    lines = lines[1:]

    with open(input_file, 'w') as file:
        file.writelines(lines)

def sort_info_per_line(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    end_list = []

    for i in range(len(lines)):
        utility_list = lines[i].split(";")
        end_list.append(f"{utility_list[1]};{utility_list[0]};{utility_list[5]};{utility_list[6]};{utility_list[7]};{utility_list[8]};{utility_list[9]};{utility_list[10]}\n")
    
    with open(input_file, 'w') as file:
        file.writelines(end_list)

def folder_create_json(input_file):
    os.mkdir("json_files")

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for x in range(1, 7):
        end_list = []

        for i in range(len(lines)):
            utility_list = lines[i].splitlines()
            utility_list = utility_list[0].split(";")
            
            value = "\t\t{ label: " + f'"{utility_list[0]} ({utility_list[1]})", y: ' + str(utility_list[x+1]) + " }"
                
            if i < len(lines)-1:
                value = value + ","
            
            value = value + "\n"
                
            end_list.append(value)


        with open(f"json_files/region_debit{x}.json", 'w') as file:
            file.writelines("[\n")
            file.writelines(end_list)
            file.writelines("];\n")

download_file(args.lien, args.destination)
delete_first_line(args.destination)
sort_info_per_line(args.destination)
folder_create_json(args.destination)