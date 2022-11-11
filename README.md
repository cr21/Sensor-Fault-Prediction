
### Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class
indicates that the failure was caused by something else.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

| True class      | Positive |   Negative |
| --------------- | -------- | ---------- |
| Predicted Class |          |            |
| Positive        |          | Cost 1     |
| Negative        | Cost 2   |            |


Cost 1 = 10 and Cost 2 = 500

- The total cost of a prediction model the sum of `Cost_1` multiplied by the number of Instances with type 1 failure and `Cost_2` with the number of instances with type 2 failure, resulting in a `Total_cost`. In this case `Cost_1` refers to the cost that an unnessecary check needs to be done by an mechanic at an workshop, while `Cost_2` refer to the cost of missing a faulty truck, which may cause a breakdown. 
- `Total_cost = Cost_1 * No_Instances + Cost_2 * No_Instances.`

- From the above problem statement we could observe that, we have to reduce false positives and false negatives. More importantly we have to **reduce false negatives, since cost incurred due to false negative is 50 times higher than the false positives.**

### Solution Proposed 
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.
## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions


## How to run?
Need MongoDB in your Local System, We are deploying project using ECR, EC2 so we need AWS account

# Project Workflow
![image](/flowcharts/0_Sensor%20Training%20Pipeline.png)
## Data Collections
![image](/project_architecture_diagrams/DataCollection.png)


## Project Archietecture
![image](/project_architecture_diagrams/ProjectArchitecture.png)


## Deployment Archietecture
![image](/project_architecture_diagrams/deploymentArchitecture.png)

### Step 1: Clone the repository
```bash
git clone https://github.com/cr21/Sensor-Fault-Prediction.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n venv python=3.7.6 -y
```

```bash
conda activate venv
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL="MONGO_URL_FOR_DATASET"

```

### Step 5 - Run the application server
```bash
python app.py
```

### Step 6. Train application
```bash
http://localhost:8080/train

```

### Step 7. Prediction application
```bash
http://localhost:8080/predict

```

## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> . 

```

3. Run the Docker image
```
docker run -d -p 8080:8080 <IMAGE_NAME>
```

To run the project  first execute the below commmand.
MONGO DB URL: 

Linux/MAC user

```
export MONGO_DB_URL=mongodb+srv://cr:root@cluster0.ufj8ovv.mongodb.net/?retryWrites=true&w=majority
```

then run 
```
python main.py
```
