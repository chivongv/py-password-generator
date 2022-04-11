#!/usr/bin/python3

import sys, getopt
import string
import secrets

class NoPasswordOptionsError(Exception):
    """Raised when all options to generate password are false: uppercase, lowercase, digits, symbols"""
    pass

class PasswordLengthIsZeroError(Exception):
    """Raised when the generated password length is smaller than or equals to 0. Password length must be greater than 0."""
    pass

def print_usage():
    print('main.py -o <outputfile> -n <password_length> -t <number_of_passwords> -u <true/false> -s <true/false> -l <true/false> -d <true/false>')

def get_pw_options_inputs(msg: string):
    variable = True
    v = input(msg).lower().strip()
    if v == 'false' or v == 'f':
        variable = False
    return variable


def generate_password(length=8, uppercase = True, symbols = True, lowercase = True, digits = True):
    if(not symbols and not uppercase and not lowercase and not digits):
        raise NoPasswordOptionsError("There must be at least one equals to true of the options: uppercase, lowercase, digits, symbols")

    if(length <= 0):
        raise PasswordLengthIsZeroError("Password length must be greater than 0.")

    combination = ''
    if(lowercase):
        combination += string.ascii_lowercase
    if(digits):
        combination += string.digits
    if symbols:
        combination += string.punctuation
    if uppercase:
        combination += string.ascii_uppercase

    combination_length = len(combination)
    new_password = ''
    for _ in range(length):
        # secrets.randbelow works better than random for security purposes
        # https://docs.python.org/3/library/random.html
        new_password += combination[secrets.randbelow(combination_length)]
    return new_password

def main():
    outputfile = ''
    #default all are true
    upper = syms = lower = digs = True
    length = 8
    times = 1
    # if we have args, read flags and set values
    if (len(sys.argv) >= 2):
        try:
            # no : after o means we don't expect anything after the flag
            opts, args = getopt.getopt(sys.argv[1:], "ht:n:o:u:s:l:d:", ["times", "length", "uppercase", "symbols", "digits", "lowercase", "ofile"])
        except getopt.GetoptError:
            print_usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print_usage()
                sys.exit()
            elif opt in ('-t', "--times"):
                times = int(arg or 1)
            elif opt in ('-n', '--length'):
                length = int(arg or 8)
            elif opt in ('-u', '--uppercase'):
                if(arg == 'false' or arg == 'f'):
                    upper = False
            elif opt in ('-s', '--symbols'):
                if(arg == 'false' or arg == 'f'):
                    syms = False
            elif opt in ('-l', '--lowercase'):
                if(arg == 'false' or arg == 'f'):
                    lower = False
            elif opt in ('-d', '--digits'):
                if(arg == 'false' or arg == 'f'):
                    digs = False
            elif opt in ('-o', '--ofile'):
                outputfile = arg
    # if no args then get inputs from user
    else:
        n = int(input("Enter password length(default 8): ") or 8)
        if(n <= 0):
            print("Password length can not be smaller than 1. Default 8 will be used.")
        elif(n>0):
            length = n
        t = int(input("Enter the number of times for password to be generated(default 1): ") or 1)
        if(t < 1):
            print("Number of times for password to be generated can not be less than 1. Default 1 will be used.")
        elif(t > 1):
            times = t
        print("Should generated password contain: ")
        upper = get_pw_options_inputs("  uppercase?(Default True) ")
        syms = get_pw_options_inputs("  symbols?(Default True) ")
        lower = get_pw_options_inputs("  lowercase?(Default True) ")
        digs = get_pw_options_inputs("  digits?(Default True) ")
        outputfile = input("Output filename: ")
        print("")

    for _,idx in enumerate(range(times)):
        try:
            password = generate_password(length, upper, syms, lower, digs)
            if(outputfile):
                with open(outputfile, 'a') as f:
                    f.write(password + '\n')
            else:
                print("#" + str(idx+1), password)
        except NoPasswordOptionsError as e:
            print(e)
            sys.exit(1)
        except PasswordLengthIsZeroError as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
   main()