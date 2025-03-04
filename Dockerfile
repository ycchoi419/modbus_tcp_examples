# Use Python 3.12 as the base image
FROM python:3.12-slim

ENV HOST=10.0.100.20 \
    AMS_PORT=503

WORKDIR /app

RUN pip install pymodbus pyModbusTCP

COPY bms/ bms/

# Run the script
CMD ["python", "bms/modbus_master_ams.py"]
# CMD ["sleep", "infinity"]