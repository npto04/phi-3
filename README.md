# Assessing LLM with LangChain
## Running the notebook examples
The notebook examples are available in the `notebooks` folder. To run the examples, you need to have the following dependencies installed:
- Python 3.10 or higher
- Docker
- GPU with CUDA support (optional). If you don't have a GPU, you can still run the examples, but it will be slower. Adjust scripts to run on CPU.

To run the examples, follow these steps:
1. Clone the repository
2. Open a terminal and navigate to the repository folder
3. Run the following command to start the Jupyter notebook server:
```bash
docker compose up -d jupyter-notebook
```
4. Pull the model and be set up to run:
```bash
sh startup.sh
```
or
```bash
docker compose exec -d ollama-server ollama pull llama3:instruct
```
To-do:
- [ ] Add request to backend API
- [ ] Address issues with the model
- [ ] Integrate solutions with Chatbot API
