# YouTube DevOps Platform

Automated YouTube analytics system that delivers daily statistics to Telegram.  
Built as a full DevOps project using industry-standard tools.

## What it does

- Fetches daily stats from YouTube channels (Funny Damon Show 1.7M+ subscribers, Damon Dylan 339K)
- Sends automated Telegram report every morning at 9:00 AM
- Uses Google Gemini AI to analyze channel performance and trends
- Runs 24/7 on AWS EC2 in Docker containers

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Terraform** | Provision AWS EC2 server |
| **Ansible** | Automate server configuration |
| **Docker & Docker Compose** | Run app in containers |
| **Nginx** | Reverse proxy web server |
| **GitHub Actions** | CI/CD — auto deploy on every commit |
| **Python** | Bot logic, YouTube API integration |
| **Telegram Bot API** | Daily notifications |
| **YouTube Data API v3** | Fetch channel statistics |
| **Groq AI (LLaMA 3)** | Analyze channel performance and trends |

## Architecture

```
GitHub → GitHub Actions → AWS EC2
                              ├── Docker: Telegram Bot (Python)
                              └── Docker: Nginx
```

## Project Structure

```
youtube-devops-platform/
├── terraform/          # AWS infrastructure as code
├── ansible/            # Server configuration
├── app/                # Python Telegram bot
│   ├── bot.py
│   ├── requirements.txt
│   └── Dockerfile
├── nginx/              # Nginx configuration
├── .github/workflows/  # CI/CD pipeline
└── docker-compose.yml
```

## Setup

### 1. Infrastructure
```bash
cd terraform
terraform init
terraform apply
```

### 2. Configure server
```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

### 3. Environment variables
Create `.env` file:
```
YOUTUBE_API_KEY=your_key
TELEGRAM_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
GROQ_API_KEY=your_groq_key
```

### 4. Deploy
```bash
docker-compose up -d
```

CI/CD automatically deploys on every push to `main` branch.

## Author

Marta Dzekevich — [GitHub](https://github.com/marta77784)
