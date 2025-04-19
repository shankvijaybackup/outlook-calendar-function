# Start with the Python 3.8 base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.8

# Set the working directory to /home/site/wwwroot
WORKDIR /home/site/wwwroot

# Copy the requirements file into the container at /home/site/wwwroot
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Start the Azure Functions app
CMD ["python", "function_app.py"]
