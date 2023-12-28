FROM python:3.11.4-slim-bullseye as prod


RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

# Create .env file
RUN echo "REVERSE1999_DAMAGE_CALCULATOR_RELOAD=True" > /app/src/.env

CMD ["/usr/local/bin/python", "-m", "reverse1999_damage_calculator"]

FROM prod as dev

RUN poetry install
