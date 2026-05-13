# --------------------------------------------------------------
# 1) Base image
# --------------------------------------------------------------
# Use the official lightweight Python image (Alpine is too small for
# many scientific wheels, so we start from Debian‑slim).
FROM python:3.11-slim

# --------------------------------------------------------------
# 2️) Set a non‑root user (good practice)
# --------------------------------------------------------------
ARG USERNAME=momod
ARG UID=1000
ARG GID=1000

RUN groupadd -g ${GID} ${USERNAME} \
    && useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

# --------------------------------------------------------------
# 3️3) Install system dependencies
# --------------------------------------------------------------
# - build-essential: needed for compiling some wheels
# - git, wget: handy utilities
# - libgl1-mesa-glx & libglib2.0-0: required by matplotlib, opencv, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        wget \
        curl \
        ca-certificates \
        # libgl1-mesa-glx \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------
# 4️) Install Python packages (Jupyter + common data‑science stack)
# --------------------------------------------------------------
# Pin versions where you want reproducibility; otherwise let pip pick latest.
RUN pip install --no-cache-dir \
        notebook==7.2.2 \
        jupyterlab==4.2.5 \
        ipykernel==6.29.5 \
        numpy==2.1.0 \
        pandas==2.2.2 \
        matplotlib==3.9.2 \
        seaborn==0.13.2 \
        scikit-learn==1.5.2 \
        scipy==1.14.1 \
        plotly==5.24.1 \
        tqdm==4.66.5

RUN pip install --no-cache-dir torch==2.3.0

RUN pip install --no-cache-dir tensorflow==2.16.1

RUN pip install --no-cache-dir eli5==0.16.0

# --------------------------------------------------------------
# 5️) Create a Jupyter kernel for the non‑root user
# --------------------------------------------------------------
USER ${USERNAME}
RUN python -m ipykernel install --user --name=${USERNAME} --display-name="Python (docker)"

# --------------------------------------------------------------
# 6️) Set working directory (where notebooks will live)
# --------------------------------------------------------------
WORKDIR /home/${USERNAME}/work

# --------------------------------------------------------------
# 7️) Expose the Notebook port
# --------------------------------------------------------------
EXPOSE 8888

# --------------------------------------------------------------
# 8️) Entrypoint – start Jupyter Notebook
# --------------------------------------------------------------
#   * --ip 0.0.0.0   – listen on all interfaces (required for Docker)
#   * --no-browser  – don’t try to open a browser inside the container
#   * --NotebookApp.token='' – disable token auth (use with care!)
#   * --NotebookApp.password='' – disable password auth (use with care!)
#   * --allow-root   – needed only if you run as root (we don’t)
CMD ["jupyter", "notebook", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--NotebookApp.token=''", \
     "--NotebookApp.password=''", \
     "--NotebookApp.allow_origin='*'"]

