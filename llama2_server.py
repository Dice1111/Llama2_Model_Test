from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os
from dotenv import load_dotenv
from huggingface_hub import login

# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_KEY")
login(token=HF_TOKEN)

# Initialize FastAPI app
app = FastAPI()


# Load the LLaMA 2 Chat model and tokenizer
model_name = "meta-llama/Llama-2-7b-chat-hf"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=HF_TOKEN,
        device_map="auto",
        load_in_8bit=True
    )
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Request body model
class Prompt(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "Healthy"}

@app.post("/generate")
def generate_text(prompt: Prompt):
    try:
        input_prompt = f"<s>[INST] {prompt.prompt} [/INST]"
        result = pipe(input_prompt)
        return {"generated_text": result[0]["generated_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
