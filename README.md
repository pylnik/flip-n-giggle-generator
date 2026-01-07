# Flip-n-Giggle Generator

A Python application that generates children's flip books where each page contains a "noun verb noun" sentence. The pages are designed to be cut into three parts, allowing each word to flip independently to create humorous sentence combinations.

## Features

- 🎨 Generate random "noun verb noun" sentences
- 📚 Create complete flip books with multiple pages
- 🖨️ Format output for printing and cutting
- 🎲 Thousands of possible funny combinations
- ⚙️ Customizable word lists
- 📊 Statistics on possible combinations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/flip-n-giggle-generator.git
cd flip-n-giggle-generator
```

2. No external dependencies required - uses Python standard library only!

## Usage

### Basic Usage

Generate 10 flip book pages and display them:
```bash
python main.py
```

### Generate Custom Number of Pages

```bash
python main.py -n 20
```

### Save to File

```bash
python main.py -o myflipbook.txt
```

### Different Output Formats

List format (simple):
```bash
python main.py -f list
```

Print format (with cut lines):
```bash
python main.py -f print
```

### Show Statistics

```bash
python main.py --show-stats
```

## Example Output

```
===========================================================
              FLIP-N-GIGGLE BOOK
===========================================================

                     Page 1
-----------------------------------------------------------
|                     The cat                        |  <- Cut here
-----------------------------------------------------------
|                     tickles                        |  <- Cut here
-----------------------------------------------------------
|                    a balloon                       |
-----------------------------------------------------------
```

## How to Make Your Flip Book

1. Run the program and save output to a file
2. Print the pages
3. Cut along the lines marked "Cut here"
4. Stack the pages and bind them on the left side
5. Flip each section independently to create funny sentences!

## Project Structure

```
flip-n-giggle-generator/
├── flipbook/
│   ├── __init__.py
│   ├── generator.py      # Core sentence generation logic
│   ├── word_lists.py     # Default word lists
│   └── formatter.py      # Output formatting
├── main.py               # Command-line interface
├── README.md
└── requirements.txt
```

## Customization

You can customize the word lists by editing [flipbook/word_lists.py](flipbook/word_lists.py) or by creating your own lists and passing them to the `FlipBookGenerator` class.

## Python API

```python
from flipbook.generator import FlipBookGenerator
from flipbook.formatter import FlipBookFormatter

# Create generator
generator = FlipBookGenerator()

# Generate sentences
sentences = generator.generate_book(num_pages=5)

# Format for output
formatter = FlipBookFormatter(generator)
print(formatter.format_for_print(sentences))
```

## Requirements

- Python 3.8 or higher

## License

MIT License - feel free to use this for educational purposes!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Ideas for Enhancement

- Add support for different sentence structures
- Create PDF output with proper page formatting
- Add illustrations or emoji support
- Web interface for generating flip books
- Multi-language support
