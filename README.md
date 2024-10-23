<h1> Markdown Enhancer </h1>

<h2>Table of Contents</h2>

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [How to Use](#how-to-use)
- [Example](#example)
- [Customization](#customization)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This Python script is designed to enhance Markdown files (.md) by applying a visually appealing style to the content while maintaining the original formatting. It provides two main functionalities: enhancing Markdown files with a new layout and styles, and reverting enhanced files back to their original Markdown format.

## Features

- **Enhancing Markdown Content**: 
  - Adds a hero section with the title of the document.
  - Generates a navigation bar from the second-level headers (H2).
  - Applies custom CSS styles for better readability and aesthetics.
  - Converts code blocks into styled presentation.
  - Preserves original Markdown content as a base64-encoded comment.

- **Reverting Enhanced Markdown Content**: 
  - Returns enhanced files to their original format with Markdown styling.
  - Removes all the applied styles and enhancements.

## Getting Started

### Prerequisites

- Python 3.x
- Text editor to read and edit Markdown files.

### Installation

1. Clone the repository or download the script to your local machine.
2. Ensure you have Python installed and accessible in your command line.

### How to Use

Run the script from the command line, passing either `enhance` or `revert` as an argument.

```bash
python script.py [enhance|revert]
```

- To **enhance** Markdown files:
  - Place your `.md` files in the same directory as the script.
  - Execute the command:
    ```bash
    python script.py enhance
    ```
  - This will create new files with `_enhanced` appended to their names.

- To **revert** enhanced Markdown files:
  - Execute the command:
    ```bash
    python script.py revert
    ```
  - This will convert files back to their original format, creating new `.md` files without the `_enhanced` suffix.

## Example

1. **Enhancing a Markdown File:**

   If you have a file named `example.md`, the command:
   ```bash
   python script.py enhance
   ```
   will create a new file named `example_enhanced.md` with the enhancements applied.

2. **Reverting the Enhanced File:**

   If you then run:
   ```bash
   python script.py revert
   ```
   it will convert `example_enhanced.md` back to the original `example.md`.

## Customization

You can modify the CSS styles in the `css_styles` variable of the `enhance_markdown` function to suit your aesthetic preferences. This allows you to customize how headings, code blocks, and other elements are displayed.

## Limitations

- The script does not currently handle Markdown files that include non-standard syntax or very complex structures.
- Ensure that the Markdown files are properly formatted to be effectively enhanced or reverted.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Your feedback and improvements are welcome!

## License

This project is licensed under the [Apache 2.0 License](./LICENSE).