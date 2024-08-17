# Documentation


## How To Run The App
1. Clone the Repository -> ```git clone https://github.com/yogiyogh3957/check_referral_fraud.git```
2. make sure the data cloned perfectly
   ![Screenshot 2024-08-17 at 15 55 03](https://github.com/user-attachments/assets/9a507cf7-fffe-4ebc-8d6e-9743ef83ddab)
3. Build the Dockerfile -> ```docker build --tag python-docker .```
4. Success Build the Dockerfile
   ![Screenshot 2024-08-17 at 15 59 39](https://github.com/user-attachments/assets/3e5a2c7e-fb3a-4017-a6bf-d47b089f16d4)
5. Get The Image ID -> ```docker images```
   ![Screenshot 2024-08-17 at 16 00 46](https://github.com/user-attachments/assets/aef09c91-cd26-40f4-a2a0-411f3f9dad91)
6. Run the Docker Images -> ```docker run -p 8000:8000 [Images ID]```
7. The Containers have been running, and access the app via url -> ```0.0.0.0:8000```
   ![Screenshot 2024-08-17 at 16 04 27](https://github.com/user-attachments/assets/ff6d0f0e-0d36-4d6f-a8e7-720248658c25)
8. Access the App and download the result
   <img width="1378" alt="Screenshot 2024-08-17 at 16 06 27" src="https://github.com/user-attachments/assets/65a1bfad-c367-441f-841b-a6bc1f4554bd">

