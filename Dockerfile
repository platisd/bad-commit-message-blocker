FROM python:3.7-slim-buster

RUN apt-get update
RUN apt-get -y install git

RUN pip3 install textblob
RUN python3 -m textblob.download_corpora
# nltk_data ends up in /root so python can't find it
RUN ln -s /root/nltk_data /usr/local/nltk_data

COPY entrypoint.sh /blocker/entrypoint.sh
COPY bad_commit_message_blocker.py /blocker/bad_commit_message_blocker.py

ENTRYPOINT ["/blocker/entrypoint.sh"]
