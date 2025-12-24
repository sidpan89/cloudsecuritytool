install:
npm install

backend:
uvicorn backend.app.main:app --reload

format:
npx prettier -w src
