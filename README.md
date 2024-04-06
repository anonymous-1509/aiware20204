## Setup
### Prerequisites
- Python3
- Pip

## Usage
To collect the dataset, run:
`collect_refactorings.sh`

## RQ1
To generate refactorings and collect code smells, run the following code:
```
cd RQ1

python3 inference.py

extract_code_smells.sh
```

### Note
Depending on the size of the test.jsonl file, this could take several days to weeks. We include our code smell metrics in the RQ1 folder under code_smells.

## RQ2
The script we use for fine-tuning is given in RQ2: `fine_tuning.ipynb`

## RQ3
To generate refactorings with the fine-tuned model, first, adjust the path at the beginning of `inference_finetuned.py`, then run.
