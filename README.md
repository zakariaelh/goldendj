# Setup 

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

# Run goldendj 
You have two options: 
1. *(easy)* Run everything using Docker
2. *(less easy)* Run python script directly

## Run everything with Docker
Build and run the container image. 
```
docker build -t goldendj .
docker run -p 3000:3000 goldendj
```
Now, you have a container running on port 3000. Remember that we opened this port to the public using `ngrok` during setup. 
You can call the number now.

## Run directly using python

### Install poetry 
Make sure you have poetry installed. Follow the instruction [here](https://python-poetry.org/docs/)

### Set up your virtual environment 
```
python3 -m venv env
```

### Install dependencies
```
poetry install
```

### Run the server with uvicorn 
```
uvicorn main:app  --port 3000 --reload
```
