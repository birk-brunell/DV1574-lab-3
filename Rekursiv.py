# Kod skriven av Birk Brunell
# Rekursiv labb 3
# Estimerad tid: 30 min
# Faktisk tid: 30 min

def recursive_max(lst):
    """Finds Max"""
    print("start")
    if len(lst) == 0:
        print("Empty List")
        return None

    elif len(lst) == 1:
        return lst[0]

    else:
        lst_max = recursive_max(lst[1:])
        return lst_max if lst_max > lst[0] else lst[0]


def lst_getter():
    """etffdg"""
    try: 
        lst = [] 
        print("Input integers to add them to the list. Finish by typing something that is not an integer.")
        while True: 
            lst.append(int(input())) 
          
    except: 
        print("List created")
        return lst


def main():
    """Main Program"""
    lst = lst_getter()
    print("List: ", lst)

    lst_max = recursive_max(lst)
    print("List max: ", lst_max)


main()