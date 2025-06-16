FROM continuumio/miniconda3

ARG OPENAI_API_KEY
ARG LANGCHAIN_API_KEY
ARG SERVER_PORT
ARG PERSIST_DIR

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
ENV SERVER_PORT=${SERVER_PORT}
ENV PERSIST_DIR=${PERSIST_DIR}

WORKDIR /app

RUN mkdir -p /tmp/gradio && chmod 777 /tmp/gradio

COPY environment.yml .
COPY . .

RUN conda env create -f environment.yml && conda clean -afy

ENV PATH /opt/conda/envs/kbank-poc/bin:$PATH
ENV CONDA_DEFAULT_ENV=kbank-poc
ENV PYTHONPATH=/opt/conda/envs/kbank-poc/lib/python3.10/site-packages

CMD ["python", "main.py"]