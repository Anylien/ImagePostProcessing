## Image Postprocessing Workflow Diagram

```mermaid
%% commet in mmd files

graph TD
A[Event JSON]
B[AWS Lambda function]
C[JSON images keys file from S3]
D[Original images files from S3]
E[Scenes settings from DynamoDB]
F[Scenes]
G[Detectron2 analysis results data from DynamoDB]
H[Post-processing settings from .ini file]
I[Post-processed images scenes - Processing made in lambda]
U[Post-processed images put in S3]
V[Scenes configurations data put in DynamoDB]

A -->|triggers | B
B -->|loads in lambda from Event JSON | C
B -->|loads in lambda | E
B -->|loads in lambda | G
B -->|loads in lambda | H
C -->|loads in lambda | D
D -->|is used to create in lambda | F
E -->|is used to create in lambda | F
F -->|is used to create in lambda | I
G -->|is used to create in lambda | I
H -->|is used to create in lambda | I
I -->|put in S3 | U
I -->|put in DynamoDB | V

style A fill: green
style B fill: yellow
style I fill: red

```

## Trigger

`2022-07-12_13_04_43_cest` updatetime of the config

s3://aps-video-stream-capturing/

config/

config__ovanet_camera206__6ea07d73-53b8-494b-ae02-4676c9c95e97.json

config__ovanet_cameraxxx__2f82a624-2eda-44a0-9808-d855088186cf.json

## Output

s3://aps-video-stream-capturing/

captures/

ovanet_camera206__6ea07d73-53b8-494b-ae02-4676c9c95e97__2022-07-12_13_04_43_cest/

ovanet_camera206__6ea07d73-53b8-494b-ae02-4676c9c95e97__2022-07-12_13_04_43_cest.mp4


log/

ovanet_camera206__6ea07d73-53b8-494b-ae02-4676c9c95e97__2022-07-12_13_04_43_cest/

ovanet_camera206__6ea07d73-53b8-494b-ae02-4676c9c95e97__2022-07-12_13_04_43_cest.log
