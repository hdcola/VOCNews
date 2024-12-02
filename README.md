# VOCNews

## Project description

This project will complete a news site like this one for Chinese people, it will have a front end that uses Gatsby and React to display news. There won't be a full backend, but there will be a service that gets news via RSS, translates it into Chinese, and updates the news site through a publishing system.

## Technologies used

- Front end: Gatsby, React, Tailwindcss
  - Telegram Channel: User can subscribe to the channel to get the latest news
  - Telegram Bot: Monitor the operation of the system
- Back end: Nodejs
  - Python: News crawling, content analysis, translation, publishing
  - requests: Get news list from RSS
  - feedparser: Parse RSS
  - BeautifulSoup: Extract news content
  - lxml: Parse HTML
  - lxml-html-clean: Clean HTML
- Cloud service: Cloudflare Pages, Cloudflare Images, Cloudflare Function
  - MongoDB: Store news list
  - Doppler: Store environment variables and secrets
  - OpenAI/Ollama: use GPT 3.5 or QWen2 7b to translate news content
  - Telegraph: Publish news content
  - Docker & Enroot: Run the service
- CI/CD: React Testing Library, jest
  - pytest: Test the Python code 
  - GitHub Actions: CI and CD
  - PDM: Python package management

## Installation

### News Feed Service

#### Setup Environment

The following instructions are based on Debian 12, and other systems may vary. Please check your system version via `/etc/os-release`.

##### Instlal PDM

```bash
sudo apt install python3-pdm
```

##### Install ollama and pull the model

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2:7b-instruct
```

##### Install enroot

```bash
arch=$(dpkg --print-architecture)
curl -fSsL -O https://github.com/NVIDIA/enroot/releases/download/v3.5.0/enroot_3.5.0-1_${arch}.deb
curl -fSsL -O https://github.com/NVIDIA/enroot/releases/download/v3.5.0/enroot+caps_3.5.0-1_${arch}.deb # optional
sudo apt install -y ./*.deb
```

##### Install VOCNews

```bash
rm *.sqsh
enroot import docker://ghcr.io#hdcola/vocnews:latest
enroot create -f --name vocnews hdcola+vocnews+latest.sqsh
```

##### Start VOCNews

```bash
enroot start -e DOPPLER_TOKEN=your_doppler_token -m host_dir:/home/yourname vocnews
```

If you want to enter the container, you can use the following command:

```bash
enroot start vocnews /bin/bash
```

#####


## Special features

- [x] Get news list from RSS
- [x] Store news list to MongoDB and get updated news list
- [x] Analyzing news content and extracting reading views through crawlers
- [x] Translate news content into Chinese with OpenAI or Ollama's local LLM
- [x] Convert HTML to Telegraph format and publish to Telegraph
- [x] Publish news to the Telegram channel
- [x] Fully automated updating and operation
- [ ] Share to social media can be friendly to display content
- [ ] Automatic posting to websites and Telegram channels
- [ ] Telegram Bot allows you to monitor the operation of your system

## Use Case

![UseCase](imgs/usecase.png)

## System Architecture

![SystemArchitecture](imgs/systemarchitecture.png)