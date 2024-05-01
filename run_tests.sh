#!/bin/bash

docker build -t meal_prep_ai .

docker run --rm -v "$(pwd)":/app meal_prep_ai pytest /app/tests/
