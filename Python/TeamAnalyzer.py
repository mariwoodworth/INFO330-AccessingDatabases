import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

connection = sqlite3.connect("../pokemon.sqlite")

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    
    # Selecting name from pokemon
    cursor = connection.cursor()
    sql = "SELECT name FROM pokemon WHERE pokedex_number = " + arg + ";" 
    cursor.execute(sql)
    results = cursor.fetchone()

    poke_name = results[0] # each pokemon's name w/o ',;
    print("Analyzing " + arg) # print analyzing statement

    # Selecting pokemon's types for each one
    sql1 = "SELECT type1 FROM pokemon_types_view WHERE name = '" + poke_name + "';"
    sql2 = "SELECT type2 FROM pokemon_types_view WHERE name = '" + poke_name + "';"
    
    cursor.execute(sql1)
    type1result = cursor.fetchone() # fetching pokemon's type1
    poke_type1 = type1result[0]

    cursor.execute(sql2)
    type2result = cursor.fetchone() # fetching pokemon's type2
    poke_type2 = type2result[0]

    # Fetching against values to compare
    sql3 = "SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name = '" + poke_type1 + "' AND type2name = '" + poke_type2 + "'"

    # Comparing against values
    for index, against in enumerate(types):
        strong = []
        weak = [] 
        cursor.execute(sql3) # executing sql
        poke_against = cursor.fetchone() # table of against values

        for j, k in enumerate(poke_against): # cycle through against to append to strong/weak
            if k > 1:
                strong.append(types[j])
            elif k < 1:
                weak.append(types[j])

    print(poke_name + " (" + poke_type1 + " " + poke_type2 + ") is strong against", strong, "but weak against", weak)

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

