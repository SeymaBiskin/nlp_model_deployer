FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel
RUN pip install --upgrade pip 

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt --no-cache-dir \
    && python -m nltk.downloader punkt

EXPOSE 4000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
