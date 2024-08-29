# **Car Sales Conversation Information Extractor and Analyzer.**
An NLP based Car Sales Conversation Information Extractor and Analyzer.

***Objective:***

  Create a tool that can process car sales conversation transcripts and extract specific types of
  information related to customer requirements, company policies discussed, and customer
  objections without extensive training data.

***Requirements***

  1. Input: The system should accept conversation transcripts in plain text or PDF format.
  2. Processing: Implement natural language processing techniques to analyze the text and extract relevant information.
  3. Output: Generate a structured output (JSON) containing the extracted information.
  4. Frontend: Develop a simple web interface where users can upload transcript files and view results.
  5. Participants will be provided with a set of transcriptions to develop the pipeline, and their solution will be evaluated on similar set of hidden test files.

***Information to Extract***
  
  1. Customer Requirements for a Car:
     
    ○ Car Type (Hatchback, SUV, Sedan)
    ○ Fuel Type
    ○ Color
    ○ Distance Travelled
    ○ Make Year
    ○ Transmission Type
  
  2. Company Policies Discussed:
   
    ○ Free RC Transfer
    ○ 5-Day Money Back Guarantee
    ○ Free RSA for One Year
    ○ Return Policy
  
  3. Customer Objections:
   
    ○ Refurbishment Quality
    ○ Car Issues
    ○ Price Issues
    ○ Customer Experience Issues (e.g., long wait time, salesperson behaviour)

***Implementation:***

  * Used ***sapCy*** python package for NLP data matching process.
    *   In this NLP process i had used few custom data to train the model for our specific requirement 
  * Used ***Flask*** to build web Application to deploy the model.
  * Used ***Ngrok*** for Port-forwording

***Output:***

[![Watch the video](https://github.com/Srivikkash/Car_Sales_Conversation_Information_Extractor_and_Analyzer/blob/7e72170852075a2936f349212156070073e4fd21/output_Video/final_output.mp4)
  
***Conclusion:***

This is an project that has been developed for ***Niral 2024 Hackathon*** conducted by *Anna university, Guindy* 

By developing this project i had developed an automation system to simplify the task  of the Car salers by gathering the requirements of the customer from their conversation PDF.

