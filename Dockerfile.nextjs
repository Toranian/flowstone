# Use the official Node.js image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json files
COPY ./code/web/package*.json ./

# Install dependencies with the legacy peer dependencies flag
RUN npm install --legacy-peer-deps

# Copy the rest of the project files
COPY ./code/web/ .

# Build the Next.js app
RUN npm run build

# Expose the port Next.js runs on (default is 3000)
EXPOSE 3000

# Start the Next.js server
CMD ["npm", "run", "start"]
