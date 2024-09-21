# !bin/bash
printf "Enter action to perform like\n1.runserver \n2.makemigrations \n3.migrate \n4.make&migrate \n5.startapp \n6.Run in ip address \n7.show migrations \n8.Shell \n"
read what

if [ $what -eq 1 ]; then
    python3 manage.py runserver
elif [ $what -eq 2 ]; then
    python3 manage.py makemigrations
elif [ $what -eq 3 ]; then
    python3 manage.py migrate
elif [ $what -eq 4 ]; then
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
elif [ $what -eq 5 ]; then
    echo "App Name"
    read appName
    python3 manage.py startapp $appName
elif [ $what -eq 6 ]; then
    python3 manage.py runserver 0:89
elif [ $what -eq 7 ]; then
    python manage.py showmigrations
elif [ $what -eq 8 ]; then
    python manage.py shell
fi