### Open port 3000 for Twilio 
ngrok http 3000

### Fill the values of the environment variables 
Fill the `.env.template` file with your values
For `BASE_URL`, Copy the value that ngork gives you except the `https://`
**Remember to rename it to `.env`**

### Install dependencies
```
poetry install
```

### Run Redis with Docker
```
docker run -dp 6379:6379 -it redis/redis-stack:latest
```

### Run the server with uvicorn 
```
poetry run uvicorn main:app --port 3000
```