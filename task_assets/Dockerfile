###############################################
# BASE IMAGE
###############################################
FROM python:3.11-slim
###############################################
# WORKING DIRECTORY
###############################################
RUN mkdir /app
WORKDIR /app
###############################################
# SYSTEM DEPENDENCIES
###############################################
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
###############################################
# REPOSITORY SETUP
###############################################
RUN git init /app \
 && git config user.email "test@test.com" \
 && git config user.name "test"
###############################################
# PROJECT DEPENDENCIES AND CONFIGURATION
###############################################
RUN pip install --no-cache-dir \
    pytest \
    markdown \
    Pillow \
    pyyaml \
    rich

# conftest.py — pytest config file that ensures /app/repo is on sys.path
RUN mkdir -p /app/repo && \
    printf 'import sys\nimport os\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))\n' \
    > /app/repo/conftest.py \
 && git add /app/repo/conftest.py \
 && git commit -m "Add pytest conftest config"
###############################################
# ENTRYPOINT
###############################################
ENTRYPOINT ["/bin/bash"]
