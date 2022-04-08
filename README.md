## Prerequisite

- Python 3

## Getting started

```
python3 main.py
or
python3 main.py -o gen_passwords.txt -t 5 -n 12
python3 main.py -o project_ids.txt -t 5 -n 6 -u f -s f
```

### Options

Optional flags
-t amount of times for password to be generated
-o output file name
-n length of the password
-d digits
-u uppercase
-s symbols
-l lowercase

default lowercase + digits + uppercase + symbols
default 8 characters
default 1 generated new password
default no output file, print to terminal
