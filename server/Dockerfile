FROM python:3.9.7-slim
COPY server /
COPY common/* /common/
COPY common/* /acceptor_process/
RUN python -m unittest tests/test_common.py
ENTRYPOINT ["/bin/sh"]
