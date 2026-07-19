# EMIR Local Server

## Install the dependencies
```bash
pip install -r requirements.txt
```

### Start the api in development mode
```bash
fastapi dev src/presentation/api/main.py --port 8001
```

### Build docker image
```bash
docker build -t emir-api .
```

### Run docker container
```bash
docker run -d -p 3000:80 --env-file .env emir-api
```