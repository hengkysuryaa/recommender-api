# recommender-api

## Installing Requirements
### Linux
```bash
virtualenv -p python3 venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running Server
### Linux
```bash
source venv/bin/activate
python app.py
```

### Windows
```bash
venv\Scripts\activate
python app.py
```

## API List
Serving on port 5000 (localhost:5000)
- `/` - Check API health
- `/auth` - Do simple authentication
- `/recommend` - Get personalized top products recommendation data