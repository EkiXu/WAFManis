# Use a multi-stage build for efficiency
FROM maven:3.8-jdk-8 AS builder

# Set working directory
WORKDIR /app

# Copy your project directory
COPY . .

# Install dependencies
RUN mvn clean package -DskipTest

# Build a slim JDK 8 image
FROM openjdk:8-jre-slim

# Copy the compiled JAR
COPY --from=builder /app/target/*.jar /app/app.jar

# Set the working directory
WORKDIR /app

# Expose the port where your Spring Boot application listens (usually 8080)
EXPOSE 8080

# Command to run the application
CMD ["java", "-jar", "app.jar"]