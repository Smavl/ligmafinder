# ligmafinder

Finds Unicode characters that normalize to ASCII according to PEP 3131.

## Usage

Basic compilation:
```bash
python ligmafinder.py flag
```

Compile with multiple candidates:
```bash
python ligmafinder.py -m 5 'print(flag)'
```

Get all possible candidates:
```bash
python ligmafinder.py --all flag
```

View available Unicode variants:
```bash
python ligmafinder.py --table
python ligmafinder.py --lookup
```

Check available slices for a word:
```bash
python ligmafinder.py --slices flag
```
