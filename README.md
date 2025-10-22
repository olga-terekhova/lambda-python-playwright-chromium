# lambda-python-playwright-chromium
A Docker image that creates a containerized AWS Lambda runtime with Playwright installed as a Python library with all dependencies.  
Only headless Chromium included, so the image size is only 2GB (as compared to the microsoft-playwright image at 3.5GB).    
Can be tested locally (the same image could be run locally or on AWS).  

**Project structure**:  
lambda-python-playwright-chromium/  
├─ Dockerfile  
├─ README.md  
├─ src/  
│  ├─ aws-lambda-rie  
│  ├─ lambda_function.py  
│  ├─ requirements.txt  
│  ├─ start.sh  

**What's useful here compared to other base images and walkthroughs**  

The image is build on a base Ubuntu image. Python, Python libraries, and Playwright dependencies are installed on top of it. The resulting size of the image is 2 GB.    
1) It is smaller compared to the official Microsoft Playwright image for Python at 3.51 GB, as only chromium headless is included.  
2) It is smaller compared to the official Python on Debian distribution at 3.47 GB, as this image installs Python on top of a vanilla Ubuntu image.

This image has a correct start.sh file which build Lambda Runtime emulator into the image and allows the same image be run locally and in the cloud.   
The AWS documentation example at https://github.com/aws/aws-lambda-runtime-interface-emulator/?tab=readme-ov-file#build-rie-into-your-base-image omits passing the parameter into the script, so the AWS runtime emulator doesn't see the lambda module and function handler passed in CMD.  
