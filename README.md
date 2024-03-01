# Setup 

### Set up accounts
You will need an account with each of the following services: 
- Transcriber: [Deepgram](https://deepgram.com/)
- LLM: [OpenAI](https://openai.com/)
- Synthesizer: [Elevenlabs](https://elevenlabs.io/) 
- Telephony: [Twilio](https://twilio.com) 
- Deployment: Local server [Ngrok](https://ngrok.com) Or Hosted server [Modal](https://modal.com)

#### Buy a Twilio number
- Set up an account with Twilio if you don't have one already, and purchase a phone number (~$1)

### Fill the values of the environment variables 
- Fill the `.env.template` file with your values excluding `BASE_URL`, we will come back to it.
- Rename the file to `.env`

# Run goldendj 
You have two options: 
1. *(easy)* Serverless hosting with Modal
2. *(less easy)* Local hosting with ngrok and Docker (or python)

## Serverless hosting with Modal 
- Install modal in your local environment. Modal will prompt you to set up an account *(pretty frictionless)* 
```
pip install modal
```
- We will deploy the app twice as we need the deployment URL 
```
modal run deploy
```
- Modal will build and deploy the app, and return a URL
- Take this URL and remove the `https://` part and fill the environment variables `BASE_URL` in .env file. For example: 
```
BASE_URL=myUserName--goldendj.modal.run
``` 
- Deploy again
```
modal run deploy 
```
- Go back to the Twilio Console --> Phone Numbers --> Active Phone Numbers --> Select the phone number you bought --> Update the webhook "A Call Comes in" with the new URL and `/inbound_call`, for example 
```
https://myUserName--goldendj.modal.run/inbound_call
```
- Save configuration
- Call the number! 

## Local hosting: 
- Set up the ngrok tunnel 
```
ngrok http 3000
```
- Ngrok will return a URL that looks like `https://random-ID.ngrok-free.app` 
- Remove the `https://` part and fill it in the `BASE_URL` environment variable in `.env` file
- Take this url and go back to the Twilio Console --> Phone Numbers --> Active Phone Numbers --> Select the phone number you bought --> Update the webhook "A Call Comes in" with the new URL and `/inbound_call`, for example 
```
https://random-ID.ngrok-free.app/inbound_call
```
- Save Configuration 
- Now you have option of either running everything with Docker or using python directly

### With Docker
- Uncomment the last line in `Dockerfile`. The line that looks like this: 
```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```
- Build and run the container image. 
```
docker build -t goldendj-image .
docker run -p 3000:3000 goldendj-image
```
Now, you have a container running on port 3000. Remember that we opened this port to the public using `ngrok` during setup. 
- Call the number

### With python

- Install Poetry. Follow the instruction [here](https://python-poetry.org/docs/)
- Install dependencies
```
poetry install
```
- Activate environment 
```
poetry shell
```
- Run the server with uvicorn 
```
uvicorn main:app  --port 3000 --reload
```
