import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ====== CONFIG ======
model_dir = "/checkpoint/siro/matthewchang/habitat_llm/checkpoints/2025-02-14_07-50-13-lm_instruct_base_extended/0/checkpoints/checkpoint-10000/merged-Llama-3"

# ====== DEVICE CHECK ======
if not torch.cuda.is_available():
    raise RuntimeError("CUDA is required for this script. No GPU found.")

device = torch.device("cuda")

# ====== LOAD MODEL & TOKENIZER ======
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_dir)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.float16,
    device_map=None
).to(device)

# ====== COMPILE MODEL ======
print("Compiling model...")
model = torch.compile(model)

# ====== INTERACTIVE INFERENCE ======
print(f"\nReady. Running on {device}. Type 'exit' to quit.\n")

while True:
    prompt = input(">> ")
    if prompt.strip().lower() in {"exit", "quit"}:
        break

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
        )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\n{reply}\n")
