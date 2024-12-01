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

# Runing
FROM python:$PYTHON_BASE

# From building stage copy the virtual environment
COPY --from=builder /project/.venv/ /project/.venv
ENV PATH="/project/.venv/bin:$PATH"
COPY src /project/src
CMD ["/project/.venv/bin/python", "/project/src/feedrss.py"]