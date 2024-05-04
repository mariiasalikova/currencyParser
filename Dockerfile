FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
LABEL maintainer="Mariia Salikova <salikova.work@gmail.com>"
# A directory to have app data 
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501


CMD streamlit run main.py