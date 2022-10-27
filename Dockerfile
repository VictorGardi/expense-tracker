FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install -y
RUN mkdir -p /root/.streamlit && bash -c 'echo -e "\
                                        [general]\n\
                                        email = \"your-email@domain.com\"\n\
                                        " > /root/.streamlit/credentials.toml'
RUN pip3 install -r requirements.txt
