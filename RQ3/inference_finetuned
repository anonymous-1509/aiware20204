import torch
import json
import os
import sys  
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from peft import PeftModel

model_id = "TheBloke/CodeLlama-7B-Instruct-GPTQ"

MODEL_CHECKPOINT_PATH = "/checkpoints_2000/checkpoint-120"

runtimeFlag = "cuda:0"
cache_dir = None
scaling_factor = 1.0

DEFAULT_SYSTEM_PROMPT = """You are a powerful model specialized in refactoring java code.

You must output a refactored version of the code."""

SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

B_INST, E_INST = "[INST]", "[/INST]" 
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    # rope_scaling = {"type": "dynamic", "factor": scaling_factor}
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# The following line loads the fine-tuned model from the desired checkpoint
model = PeftModel.from_pretrained(model, MODEL_CHECKPOINT_PATH)


# Specify start line if code generation exits with error
start_line = 1

with open(f"test.jsonl", "r") as test_file, open(f"generated_finetuned_refactorings.jsonl", "a") as results_file:
    lines = test_file.readlines()
    for i in range(start_line, len(lines)):
        data = json.loads(lines[i])
        before_code = data['before'] 

        # Construct the prompt with the before code
        pre_prompt = f"""# unrefactored code (java):
        {before_code}

        # refactored version of the same code:
        """
       
      
        prompt = f"{B_INST} {B_SYS}{SYSTEM_PROMPT}{E_SYS}{pre_prompt} {E_INST}"

        tokens = tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=True
        ).input_ids.to(runtimeFlag)

        max_context = int(model.config.max_position_embeddings * scaling_factor)
        max_prompt_len = int(0.85 * max_context)
        max_gen_len = int(0.10 * max_prompt_len)

        torch.cuda.empty_cache()
        generation_output = model.generate(
            input_ids=tokens,
            do_sample=False,
            max_new_tokens=max_gen_len,
            repetition_penalty=1.15,
        )

        for j in range(len(generation_output)):
            new_tokens = generation_output[j][tokens.shape[-1]:]  # Generated tokens
            response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

            results = {
                "project": data['project'],
                "commit_sha": data['commit_sha'],
                "file_name": data['file_name'],
                "input": before_code,
                "generated_response": response
            }
            results_file.write(json.dumps(results) + "\n")
