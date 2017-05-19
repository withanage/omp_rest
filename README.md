## install

```
* cd web2py/applications
* git clone https://github.com/withanage/omp_rest.git
* sudo pip2 install -r requirements.txt
```
change settings in private/appconfig.ini

check if the omp_installation files/presses is mounted into
```
/omp_rest/static/files/presses
```

## Test your installation

*  http://localhost:8000/omp_rest/api/files/230?submissionId=43
*  https://localhost:8000/omp_rest/api/backend/submissions
*  https://localhost:8000/omp_rest/api/submissions/43

