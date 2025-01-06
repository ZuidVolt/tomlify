# 🛠️ Tomlify

A simple CLI tool to quickly set up Python projects with a pre-configured `pyproject.toml` file.

## 🌟 Features

- Quick setup of `pyproject.toml` with best practices
- Custom template support via command-line options
- Custom output directory support
- Automatic backup of existing configuration files
- Comprehensive error handling and permissions verification
- Pre-configured settings for popular tools:
  - Ruff (linting)
  - MyPy (type checking)
  - PyRight (static type checking)
  - coverage (test coverage analysis)
  - radon (code complexity analysis)

## 📦 Installation

Clone the repository and make the script executable:

```bash
git clone https://github.com/zuidvolt/tomlify.git
cd tomlify
chmod +x tomlify.py
```

## 🚀 Usage

Basic usage - creates pyproject.toml in current directory:

```bash
/path/to/tomlify.py
```

Using a custom template:

```bash
/path/to/tomlify.py -t /path/to/custom/template.toml
```

Specifying an output directory:

```bash
/path/to/tomlify.py -o /path/to/project/directory
```

You can also create an alias for the script in your `.bashrc` or `.zshrc` file:

```bash
alias tomlify='/path/to/tomlify.py'
```

Command Line Options:

- `-t, --template`: Specify a custom template file path
- `-o, --output`: Specify the output directory for pyproject.toml

The script will:

1. Verify permissions and file health
2. Create a new `pyproject.toml` if none exists
3. Prompt for confirmation before overwriting an existing file
4. Automatically create a backup of any existing configuration

## 📝 License

This project is licensed under the Apache License, Version 2.0 with important additional terms, including specific commercial use conditions. Users are strongly advised to read the full [LICENSE](LICENSE) file carefully before using, modifying, or distributing this work. The additional terms contain crucial information about liability, data collection, indemnification, and commercial usage requirements that may significantly affect your rights and obligations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
