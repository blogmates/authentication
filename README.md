# Authentication
Create venv:
```
chmod +x scripts/create_venv.sh

./create_venv.sh
```

Start the app:

```
python -m flask run app/main.py
```

Start the venv:

Linux/MacOs
```
source ./venv/bin/activate
```

Windows

```
.\venv\Scripts\Activate.ps1
```

# API

### Sanity

endpoint: 
```
/sanity
```
body:
```
{

}
```
response:
```
Server is up and running
200 OK
```