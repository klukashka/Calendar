FROM node:22-alpine

RUN npm install -g nodemon

WORKDIR /frontend
COPY ./frontend/package.json ./

RUN npm install

COPY ./frontend ./

WORKDIR ./frontend

RUN npm run build

#EXPOSE 5173

CMD ["npm", "run", "dev", "--host=0.0.0.0"]