# GitHub Dependabot Alerts Exporter

This script retrieves Dependabot alerts from a GitHub organization and generates a CSV file containing the alert details. The alerts include information about security vulnerabilities in the organization's repositories.

## Prerequisites

- Python 3.11.3 or later
- Docker Image: python:3.11.3-slim
- `requests` and `dotenv` libraries (included in `requirements.txt`)
- GitHub organization name
- GitHub Personal Access Token (bearer token) with the necessary permissions to access the organization's Dependabot alerts

## Setup

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/marcel-last/github-dependabot-alert-exporter
   ```

2. Change to the project's directory:

   ```shell
   cd sec-gh-dependabot-exporter
   ```

3. Install the required dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Configuration

### dotenv

Before running the script, you need to configure the following:

1. Create a `.env` file in the project directory.

2. Open the `.env` file and add the following lines:

   ```dotenv
   GH_ORG_NAME=<github_organization_name>
   GH_ACCESS_TOKEN=<github_access_token>
   ```

   Replace `<github_organization_name>` with the name of your GitHub organization and `<github_access_token>` with your GitHub Personal Access Token (bearer token).

### Environment variables

1. Set the environment variables above for your terminal session:

```shell
export GH_ORG_NAME=<organization_name>
export GH_ACCESS_TOKEN=<access_token>
```

## Usage
### Native
Run the script using the following command:

```shell
python3 gh_dependabot_export.py
```

### Docker
Build and run the Docker container using the following command:
```shell
docker build -t sec-gh-dependabot-exporter:latest .
docker run --rm -it sec-gh-dependabot-exporter:latest
```

The script will retrieve all the Dependabot alerts for the specified organization and generate a CSV file named `dependabot_alerts_<current_date>.csv`.

## Development

To set up the development environment and execute `pip install` commands for the requirements, follow these steps:

1. Install `pyenv` to manage multiple Python versions:

   ```shell
   # macOS
   brew install pyenv

   # Ubuntu
   sudo apt-get update
   sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
     libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

   curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
   ```

2. Add `pyenv` to your shell:

   ```shell
   # macOS
   echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bash_profile

   # Ubuntu
   echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bashrc
   ```

3. Restart your shell or run the following command:

   ```shell
   # BASH
   source ~/.bash_profile  # macOS

   # ZSH
   source ~/.zshrc
   ```

4. Install Python 3.11.3 using `pyenv`:

   ```shell
   pyenv install 3.11.3
   ```

5. Set Python 3.11.3 as the global version:
   ```shell
   pyenv global 3.11.3
   ```

6. Create a new virtual environment using `venv`:

   ```shell
   # Using venv
   python3 -m venv env
   ```

7. Activate the virtual environment:

   ```shell
   source env/bin/activate
   ```

8. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

Now you can modify and run the script in your development environment.

**Note:** It's recommended to use a virtual environment to isolate the project dependencies and ensure a clean development environment. Remember to activate the virtual environment (`source env/bin/activate`) every time you work on the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
