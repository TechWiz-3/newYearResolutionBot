FROM debian:latest

# Create the bot's directory
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . /usr/src/bot

# install dependencies
RUN apt-get update # update apt-get
# install pip and python
RUN apt-get install -y python3 python3-pip git

# Install bot requirements from requirements.txt
RUN pip3 install -r ./src/requirements.txt

# Start the bot.
CMD ["python3", "./src/main.py"]