FROM python:3.12-slim
WORKDIR /course
COPY engine ./engine
COPY data ./data
ENV LAB_BIND=0.0.0.0
ENV LAB_PORT=8765
USER 65534:65534
CMD ["python", "-m", "engine.server"]
