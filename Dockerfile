FROM python:3.11

WORKDIR app/
COPY . .
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r req.txt
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["python","main.py"]
ENTRYPOINT ["/app/entrypoint.sh"]