FROM python:3

# Install process tools
RUN apt-get update && apt-get -y install procps \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash process

RUN mkdir /opt/process
RUN chown -R process:process /opt/process
RUN chmod 755 /opt/process

ENV PATH "$PATH:/home/process/.local/bin" 
WORKDIR /opt/process

# Install Python dependencies from requirements.txt if it exists
COPY requirements.txt* /opt/process
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt && rm requirements.txt*; fi


# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
EXPOSE 8000

COPY . /opt/process
RUN pip install /opt/process
USER process
WORKDIR /opt

#More work would be needed to handle the inmemory solution we are running to add workers
CMD uvicorn --workers 1 process.fastapi:app --host 0.0.0.0

