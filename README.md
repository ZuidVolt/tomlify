# 🛠️ Tomlify

A simple CLI tool to quickly set up Python projects with a pre-configured `pyproject.toml` file.

## 🌟 Features

- Quick setup of `pyproject.toml` with best practices
- Built-in backup of existing configuration
- Comprehensive error handling and logging
- Pre-configured settings for popular tools:
  - Ruff (linting)
  - MyPy (type checking)
  - PyRight (static type checking)
  - coverage (test coverage analysis)
  - radon (code complexity analysis)

## 📦 Installation

Clone the repository and make the script executable:

```bash
git clone https://github.com/yourusername/tomlify.git
cd tomlify
chmod +x tomlify.py
```

## 🚀 Usage

Navigate to your Python project directory and run:

```bash
/path/to/tomlify.py
```

You can also create an alias for the script in your `.bashrc` or `.zshrc` file:

```bash
alias tomlify='/path/to/tomlify.py'
```

This will allow you to run the script from anywhere by simply typing `tomlify` in your terminal.

The script will:

1. Create a new `pyproject.toml` if none exists
2. Prompt for confirmation before overwriting an existing file
3. Automatically create a backup of any existing configuration

## 📝 License

This project is licensed under the Apache License, Version 2.0 with important additional terms, including specific commercial use conditions. Users are strongly advised to read the full [LICENSE](LICENSE) file carefully before using, modifying, or distributing this work. The additional terms contain crucial information about liability, data collection, indemnification, and commercial usage requirements that may significantly affect your rights and obligations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📊 Logging

The tool maintains logs at `~/.logs/tomlify.log` for troubleshooting.
