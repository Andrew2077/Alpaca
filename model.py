import torch
from transformers import LLaMATokenizer, LLaMAForCausalLM, GenerationConfig

def generate_prompt(instruction: str, input_ctxt: str = None) -> str:
    if input_ctxt:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input_ctxt}

### Response:"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:"""



tokenizer = LLaMATokenizer.from_pretrained("chainyo/alpaca-lora-7b")
model = LLaMAForCausalLM.from_pretrained(
    "chainyo/alpaca-lora-7b",
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

model.eval()
if torch.__version__ >= "2":
    model = torch.compile(model)
    
    
generation_config = GenerationConfig(
    temperature = 0.1,
    top_p=0.75,
    top_k=40,
    num_beams=4,
    max_new_tokens= 128)

def response(instruction, generation_config, input_ctxt=None):
    prompt = generate_prompt(instruction, input_ctxt)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    input_ids = input_ids.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
        )

    answer = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
    return answer.split("### Response:")[1].strip()


response("Write a response that appropriately completes the request.", generation_config)