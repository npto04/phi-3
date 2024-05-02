FROM nvcr.io/nvidia/pytorch:24.03-py3
LABEL authors="neyoliveira.data@gmail.com"

RUN pip install transformers accelerate bitsandbytes sentence-transformers optimum python-dotenv langchain && pip install flash-attn --no-build-isolation

RUN pip install --upgrade jupyter ipywidgets

ENTRYPOINT ["python3", "-m", "jupyter", "notebook", "--no-browser"]