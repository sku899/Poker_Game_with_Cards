FROM python:3.6.8
COPY . .
RUN pip install Flask requests
RUN pip install flask_wtf
RUN pip install wtforms
RUN pip install email_validator
RUN pip install flask
EXPOSE 5000
ENTRYPOINT ["python", "poker_game_app.py"]
