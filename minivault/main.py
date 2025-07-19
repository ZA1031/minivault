from fastapi import FastAPI, Request
from pydantic import BaseModel
from minivault.logger import log_interaction
from datetime import datetime
import psutil
import torch
from uptime import uptime
from ollama import Client

app = FastAPI()
ollama_client = Client(host='http://localhost:11434')  # Default Ollama port

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

def query_local_model(prompt: str) -> str:
    try:
        response = ollama_client.chat(
            model='llama3',
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

@app.post("/generate", response_model=PromptResponse)
async def generate(prompt_request: PromptRequest, request: Request):
    response_text = query_local_model(prompt_request.prompt)

    log_interaction({
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt_request.prompt,
        "response": response_text,
        "client": request.client.host
    })

    return PromptResponse(response=response_text)

@app.get("/status")
def status():
    memory_used_mb = psutil.virtual_memory().used // (1024 * 1024)
    uptime_seconds = uptime()

    gpu_info = "Not Available"
    try:
        if torch.cuda.is_available():
            gpu_mem_used = torch.cuda.memory_allocated() // (1024 * 1024)
            gpu_total_mem = torch.cuda.get_device_properties(0).total_memory // (1024 * 1024)
            gpu_info = {
                "device": torch.cuda.get_device_name(0),
                "memory_used_mb": gpu_mem_used,
                "memory_total_mb": gpu_total_mem
            }
    except ImportError:
        pass  # torch not installed; ignore
    except Exception:
        pass  # GPU not available or error

    return {
        "uptime_seconds": uptime_seconds,
        "memory_used_mb": memory_used_mb,
        "gpu": gpu_info
    }

