FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y espeak

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyaudio

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN useradd shawn

USER shawn

ENV HOME=/home/shawn \
    PATH=/home/shawn/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=shawn . $HOME/app

CMD ["python","main.py"]