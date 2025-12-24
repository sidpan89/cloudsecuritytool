#!/bin/bash
if [ ! -f .env ]; then
  cp .env.example .env
  echo '.env created from example'
else
  echo '.env already exists'
fi
