ARG PYTHON_BASE=3.12-slim
FROM python:$PYTHON_BASE AS builder

# Install pdm
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

# Copy project files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# Install dependencies
WORKDIR /project
RUN pdm install --check --prod --no-editable

# Install Doppler CLI
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update && \
    apt-get -y install doppler

# Runing
FROM python:$PYTHON_BASE

# From building stage copy the virtual environment
COPY --from=builder /project/.venv/ /project/.venv
ENV PATH="/project/.venv/bin:$PATH"
COPY src /project/src
CMD ["doppler", "run", "--", "/project/.venv/bin/python", "/project/src/feedrss.py"]