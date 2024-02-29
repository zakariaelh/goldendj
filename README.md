### Set up accounts
You will need account with the following services: 
- Deepgram
- OpenAI 
- Ngrok
- Elevenlabs 
- Twilio 

### Open port 3000 for Twilio 
```
ngrok http 3000
```
This returns a URL. We call the part excluding the `https://`  the `BASEURL` 

#### Additional setup for Twilio 
- Buy a number 
- Go to the number you just purchased
- Update the Webhook URL for "A Call comes in" to `https://<YOUR BASEURL>/inbound_call`

### Fill the values of the environment variables 
Fill the `.env.template` file with your values. <br>
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