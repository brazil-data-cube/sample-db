FROM brazildatacube/geo:0.1

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y r-base && \
    rm -rf /var/lib/apt/lists/*

COPY . /devel

WORKDIR /devel

RUN pip3 install -r requirements.txt && \
    python3 setup.py install

RUN R --silent -f bdc_sample/drivers/r-scripts/install-inSitu.R