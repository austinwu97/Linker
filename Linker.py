'''
Austin Wu
aw2793
'''

import sys
from collections import OrderedDict

# Below are variables that are used to keep track of file content
mod_count = int(sys.argv[1]) #number of mods in the file, does not change
def_count = 0 #number of def in each mod, reset after each mod
use_count = 0 #number of uses in each mod, reset after each mod
current_index = 2 #keeps track of the current index of the input, starting at 2
length = len(sys.argv) #keeps track of the total length of the input
defined_symbols = OrderedDict() #dictionary that keeps track of symbols and their location
base_address = 0 #keeps track of the current base address to calculate the absolute address
symbol_address = 0 #keeps track of the final address of a symbol
symbol_rel_address = 0 #keeps track of the relative location of a symbol
use_list_len = 0 #keeps track of the use list length
program_text_len = 0 #keeps track of the program text length
mod_index = 0 #keeps track of the current mod we are on
mod_base_add = [] #list that keeps track of the base address for each module
warning = "" #optional warning message for pass 1
symbol_define_mod = {} #keep track of which module a symbol was defined in

# Below are variables that are created for pass 2 exclusively
use_list = OrderedDict() #dict that keeps track of which symbols and its respective location are used in a module
counter = 0 #used for printing
optional_message = "" #A message that could be printed if there is an error
optional_message2 = "" #A additional message that could be printed


#print("the number of mods in this file is: " + str(mod_count))
#print("length of args are: " + str(len(sys.argv)))


for i in range (0, mod_count):

    def_count = int(sys.argv[current_index])

    for defs in range(0, def_count):
        current_index = current_index + 1  # adding 1 to the current index to get the symbol
        symbol = sys.argv[current_index]  # getting the symbol

        # checking to see if the symbol has already been defined
        if (symbol in defined_symbols):
            warning = "Error: This variable is multiply defined; last value used."

        current_index = current_index + 1  # adding 1 to the current index to get the relative address
        symbol_rel_address = sys.argv[current_index]
        symbol_address = int(symbol_rel_address) + int(base_address) #calculating the final address for the symbol
        defined_symbols[symbol] = symbol_address  # adds the symbol and its location to a dictionary
        symbol_define_mod[symbol] = i


    #Use list is skipped through
    current_index = current_index + 1 #adding 1 to the current index to get the user list length
    use_list_len = int(sys.argv[current_index]) #getting the length of the use list


    #does the actual skipping of the use list
    for i in range(0,use_list_len):
        current_index = current_index + 2 #adding 2 to the index because both the symbol and rel address need to be skipped

    current_index = current_index + 1
    program_text_len = int(sys.argv[current_index]) #getting the length of the program text

    for i in range(0, program_text_len):
        current_index = current_index + 2 #adding 2 to the index because both the symbol and rel address need to be skipped

    mod_base_add.append(base_address)
    current_index = current_index + 1
    # recalculate the base address
    base_address += int(program_text_len)

    if (mod_index == mod_count - 1):
        print("Symbol Table")
        for key, value in defined_symbols.items():
            print(str(key) + "=" + str(value) + " " + warning)


    mod_index = mod_index + 1  # add 1 to the mod index

#======== This is the end of pass 1 and the start of pass 2 ===============

print("\n")
print("Memory Map")

#resetting variables for pass 2
current_index = 2
symbols_not_used = OrderedDict(defined_symbols.copy()) # keeping track of symbols that are defined but not used
print_symbols_not_used = [] #using for printing purposes


for i in range (0, mod_count):

    temp_list_warning_max_add = []  # used for generating error messages for "A"
    temp_use_not_defined = []  # used to keep track of when a symbol is not defined but used
    temp_list_dict = {}  # a dict used to check if there are duplicates
    temp_list_duplicate_symbol_values = []  # list containing duplicate symbol values
    temp_list_R_error = [] # used for generating error messages for "R"


    def_count = int(sys.argv[current_index])

    #This time we skip over the definition list
    for defs in range(0, def_count):
        current_index = current_index + 2  # adding 2 to the index because both the symbol and rel address need to be skipped

    current_index = current_index + 1
    use_list_len = int(sys.argv[current_index])

    '''
    Here is the use list. For each symbol, add it to dictionary to be used for this module only 
    '''
    for i in range(0, use_list_len):

        current_index = current_index + 1
        symbol = sys.argv[current_index]
        current_index = current_index + 1
        rel_add = sys.argv[current_index]
        use_list[symbol] = rel_add #add it to the dictionary


    current_index = current_index + 1
    program_text_len = int(sys.argv[current_index])  # getting the length of the program text

    temp_list = [] #temporary list used to store the program text

    for k in range(0, program_text_len):

        #add all content to a list
        current_index = current_index + 1
        temp_list.append(sys.argv[current_index])
        current_index = current_index + 1
        temp_list.append(sys.argv[current_index])


    #This for loop is resolving R and A instances
    for m in range(0, len(temp_list)):

        if (temp_list[m] == "R"):
            value = int(temp_list[m + 1])
            original =  value

            # iterate R
            #temp_list[m + 1] = str(value + mod_base_add[j])

            value = int(temp_list[m + 1])
            index = (m + 1) / 2
            value = abs(value) % 1000

            if (value > program_text_len):

                #use relative address instead
                value = abs(value) % 1000
                remainder = abs(value) % 1000
                new_value = int(temp_list[m+1]) - remainder
                new_value = new_value + index
                temp_list[m + 1] = new_value
                temp_list_R_error.append(1)
                temp_list_R_error.append(1)

            else:
                temp_list[m + 1] = str(int(temp_list[m + 1]) + mod_base_add[i])
                temp_list_R_error.append(0)
                temp_list_R_error.append(0)



            temp_use_not_defined.append(-1)
            temp_use_not_defined.append(-1)

        if (temp_list[m] == "A"):

            value = int(temp_list[m + 1])

            if (abs(value) % 1000 > 299):
                temp_list[m + 1] = str(value)[:1] + str(299)
                temp_list_warning_max_add.append(1) #set this as a flag so we know we need to print out the error message

            else:
                temp_list_warning_max_add.append(0) # if no error, add 0 to the warning list

            temp_use_not_defined.append(-1)
            temp_use_not_defined.append(-1)
            temp_list_R_error.append(0)
            temp_list_R_error.append(0)


        if (temp_list[m] == "I"):
            temp_use_not_defined.append(-1)
            temp_use_not_defined.append(-1)
            temp_list_R_error.append(0)
            temp_list_R_error.append(0)


        temp_list_warning_max_add.append(0) #add 0 to the warning list


    #loop to check to see if there are any duplicates

    for key, value in use_list.iteritems():

        if (value in temp_list_dict.itervalues()):

            #add to temp symbol list
            temp_list_duplicate_symbol_values.append(value)

            # remove from dict
            del temp_list_dict[old_key]

            # add new values to the dict
            temp_list_dict[key] = value

            # set the pointer to old key
            old_key = key


        else:
            temp_list_dict[key] = value
            old_key = key  # set pointer to old key

    use_list = temp_list_dict #update the current use_list


    #check for symbols that are not defined but used
    for key in use_list:

        if (key not in defined_symbols):
            new_position = (2 * int(use_list[key])) + 1
            original_value = int(temp_list[new_position])
            value = abs(original_value) % 1000
            final_value = "111"

            while (value != 777):

                new_value = final_value
                new_value = str(original_value)[0] + new_value
                temp_list[int(new_position)] = new_value
                value = abs(original_value) % 1000
                current_position = value

                # updating the pointer
                original_value = int(temp_list[2 * int(current_position) + 1])
                value = abs(original_value) % 1000
                current_position = (2 * current_position) + 1
                new_position = current_position
                temp_use_not_defined.append(key)
                temp_use_not_defined.append(key)
                temp_list_R_error.append(0)
                temp_list_R_error.append(0)



            if (value == 777):

                new_value = final_value
                new_value = str(original_value)[0] + new_value
                #current_position = int(2 * int(current_position) + 1)
                temp_list[int(current_position)] = new_value
                temp_use_not_defined.append(key)
                temp_use_not_defined.append(key)
                temp_list_R_error.append(0)
                temp_list_R_error.append(0)




        else:

            temp_use_not_defined.append(-1)
            temp_use_not_defined.append(-1)
            temp_list_R_error.append(0)
            temp_list_R_error.append(0)
            # Resolving external addresses, loop through the uses

            current_position = use_list[key]

            '''
            check to see if the last 3 digits are 777
            if so, then correct the address
            if not, pass the next iteration 
            '''
            # check to see if the last 3 digits are 777

            new_position = (2 * int(current_position)) + 1
            original_value = int(temp_list[new_position])
            value = abs(original_value) % 1000
            final_value = str(defined_symbols[key])

            while (value != 777):

                if (len(final_value) == 1):
                    new_value = "00" + final_value

                elif (len(final_value) == 2):
                    new_value = "0" + final_value

                elif (len(final_value == 3)):
                    new_value = final_value


                new_value = str(original_value)[0] + new_value
                temp_list[int(2 * int(current_position) + 1)] = new_value
                value = abs(original_value) % 1000
                current_position = value

                # updating the pointer

                original_value = int(temp_list[2 * int(current_position) + 1])
                value = abs(original_value) % 1000

                temp_use_not_defined.append(-1)
                temp_use_not_defined.append(-1)
                temp_list_R_error.append(0)
                temp_list_R_error.append(0)



            if (value == 777):

                if (len(final_value) == 1):
                    new_value = "00" + final_value

                elif (len(final_value) == 2):
                    new_value = "0" + final_value

                elif (len(final_value) == 3):
                    new_value = final_value

                new_value = str(original_value)[0] + new_value
                current_position = int( 2 * int(current_position) + 1)
                temp_list[int(current_position)] = new_value
                temp_use_not_defined.append(-1)
                temp_use_not_defined.append(-1)
                temp_list_R_error.append(0)
                temp_list_R_error.append(0)

            if (key in symbol_define_mod):
                # remove it from the dictionary
                del symbol_define_mod[key]


    temp_list_duplicate_symbol_values = list(set(temp_list_duplicate_symbol_values)) #get rid of duplicate values

    #update the module number for symbols not used

    if (i == (mod_count) - 1):

        for y in symbol_define_mod:
            message = "Warning: " + str(y)  + " was defined in module " + str(symbol_define_mod[y]) + " but never used "
            print_symbols_not_used.append(message)


    symbols_not_used.clear()


    for k in range (0, len(temp_list), 2):

        if (temp_list_warning_max_add[k] == 1):
            optional_message = "Error: A type address exceeds machine size; max legal size used"

        if (temp_use_not_defined[k] != -1):
            optional_message = "Error: " + temp_use_not_defined[k] + " was not defined; 111 used."

        if (temp_list_R_error[k] == 1):
            optional_message = "Error: Type R address exceeds module size; 0 (relative) used"

        for x in temp_list_duplicate_symbol_values:

            check_value = 2 * int(temp_list_duplicate_symbol_values[int(x)-1]) + 1

            if (check_value == int(k+1)):
                optional_message2 = " Error: Multiple symbols used here; last one used"



        print (str(counter) + ":   " + str(temp_list[k+1]) + " " + optional_message + " " + optional_message2)



        optional_message = "" #reset optional message
        optional_message2 = "" #reset optional message 2
        counter = counter + 1




    temp_use_not_defined = []
    temp_list_warning_max_add = []
    current_index = current_index + 1


    #clear the use list dictionary
    use_list.clear()


print("")


for i in print_symbols_not_used:
    print i



