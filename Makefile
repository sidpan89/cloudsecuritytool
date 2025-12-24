install:
npm install

backend:
uvicorn backend.app.main:app --reload

format:
npx prettier -w src

fetch-frontend:
bash scripts/fetch_external_frontend.sh
