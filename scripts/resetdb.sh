dropdb nike
createdb nike
./manage.py migrate
./manage.py crearCentroOrganizacion ficheros/centroOrg.txt
./manage.py crearUsuariosCentro ficheros/usuariosNew.txt
./manage.py setVacaciones 2015 22 1
./manage.py crearCalendario ficheros/festivos.txt 2015 1
