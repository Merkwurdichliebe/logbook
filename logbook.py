import sqlite3 as lite

con = lite.connect('logbook.db')
cur = con.cursor()


def list_flights():
    """Print a formatted list of all flights in the Logbook."""

    cur.execute("""SELECT Date, Immat, Temps, CDB
                FROM Vols
                INNER JOIN Avions on Avions.Avion_ID = Vols.Avion_ID
                ORDER BY Date""")
    rows = cur.fetchall()
    for row in rows:
        if row[3]:
            cdb = "CDB"
        else:
            cdb = ''
        print(row[0], row[1], pretty_time(row[2]), cdb)


def list_planes():
    """Print a formatted list of total hours flown in each plane,
    as pilot and copilot and the total of both."""

    planetotals = []
    subtotal = []

    # We run 3 queries for calculting totals:
    # one as pilot (CDB = 1), one as copilot (CDB = 0)
    # and one for the grand total (no WHERE clause)
    queries = ['WHERE CDB=1', 'WHERE CDB=0', '']

    # Run the 3 queries
    for index, query in enumerate(queries):
        sql = ' '.join(
            ("""SELECT SUM(Temps) AS 'Temps Total', Immat
            FROM Vols
            INNER JOIN Avions on Avions.Avion_ID = Vols.Avion_ID""",
            query,
            """GROUP BY Avions.Avion_ID
            ORDER BY SUM(Temps) DESC"""
            ))
        cur.execute(sql)

        # Query returns a sorted list of tuples (minutes, 'Immat')
        planetotals.append(cur.fetchall())

        # We sum the minutes (1st elements of each tuple)
        # and end up with a subtotal for each of the 3 queries
        subtotal.append(pretty_time(sum([i[0] for i in planetotals[index]])))

    # Print the table header
    print('=' * 55)
    print('{:20} {:20} {:20} '.format('Pilote', 'Élève', 'Total'))
    print('{:20} {:20} {:20} '.format(*['=' * 13] * 3))

    # We iterate using the grand total list (the one which didn't use 'WHERE')
    # which is evidently the longest one, so that we don't miss any items
    for i in range(len(planetotals[2])):
        row_output = []
        # Iterate over the three lists and format the HH:MM and Immat string
        # or add an empty string to fill in the blanks, then print the rows
        for planetotal in planetotals:
            if i < len(planetotal):
                row_output.extend((pretty_time(planetotal[i][0]), planetotal[i][1]))
            else:
                row_output.extend(('', ''))
        print('{:6} {:13} {:6} {:13} {:6} {:13}'.format(*row_output))
    
    # Print the table footer and subtotals
    print('-' * 55)
    print('{:20} {:20} {:20} '.format(*subtotal))
    print('-' * 55)


def pretty_time(minutes):
    """Converts the passed number of minutes to a string
    in the format HH:MM and returns it."""

    return '{:02d}:{:02d}'.format(*divmod(minutes, 60))


def display_menu():
    """Print the application's menu to the console."""
    
    menu = {}
    menu['1'] = "Liste des vols"
    menu['2'] = "Total heures par avion"
    menu['Q'] = "Quitter"

    while True:
        print('=' * 20)
        options = menu.keys()
        for option in sorted(options):
            print(option, menu[option])
        selection = input("]")
        if selection == '1':
            list_flights()
        elif selection == '2':
            list_planes()
        elif selection in ('Q', 'q'):
            break
        else:
            print('\nOption non valable.\n')

display_menu()
con.close()
