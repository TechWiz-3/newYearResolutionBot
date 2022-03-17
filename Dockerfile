FROM debian:latest

# Create the bot's directory
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . /usr/src/bot

# install dependencies
RUN apt-get update
RUN apt-get install -y python3 python3-pip #or some other packages too
# and other stuff if you wanna

# Install bot reqs
RUN pip3 install -r requirements.txt

# Start the bot.
CMD ["python3", "./src/main.py"]