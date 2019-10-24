FROM brazildatacube/geo:0.1

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y r-base && \
    rm -rf /var/lib/apt/lists/*

COPY . /devel

WORKDIR /devel

RUN pip3 install --upgrade pip && \
    pip install wheel && \
    pip install -e .