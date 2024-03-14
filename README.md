# FlatFinderAI

## Introduction
FlatFinderAI revolutionizes the way you search for flats in Portugal. By seamlessly integrating with Algolia, this Python application transforms vague user queries into precise search terms, delivering fast and relevant flat listings. Whether you're looking for a T2 in Almada or a cozy studio in Lisbon with breathtaking views, FlatFinderAI is your go-to solution.

## Features
- **Query Refinement:** Converts user queries into Algolia-friendly terms for efficient searching.
- **Algolia Integration:** Leverages the power of Algolia's search algorithms to fetch accurate and relevant listings.
- **OpenAI Processing:** Utilizes GPT-3.5 to process and refine search queries and interpret Algolia search results, ensuring that responses are user-friendly and informative.
- **Real-Time Listings:** Offers up-to-date information on available flats, including price, location, amenities, and more.

## How It Works
1. **User Query Input:** Start by entering your housing preferences, such as location, size, or specific amenities.
2. **Query Processing:** The system refines your input into a search query optimized for Algolia.
3. **Search Execution:** The refined query is sent to Algolia, fetching listings that match your criteria.
4. **Results Interpretation:** Utilizing OpenAI, the application interprets the raw Algolia results, presenting them in an easy-to-understand format.

## Getting Started
To get FlatFinderAI up and running on your machine, follow these steps:

1. **Clone the Repository:**
git clone https://github.com/antonioevans/FlatFinderAI.git

2. **Install Dependencies:**
Navigate to the cloned directory and install the necessary Python packages.
cd FlatFinderAI
pip install -r requirements.txt

3. **Set Up Environment Variables:**
Ensure you have valid API keys for Algolia and OpenAI. Set them as environment variables:
export ALGOLIA_APP_ID='your_algolia_app_id'
export ALGOLIA_API_KEY='your_algolia_api_key'
export GROQ_API_KEY='your_openai_api_key'

4. **Run the Application:**
python flatfinderai.py

5. **Enter Your Query:**
Follow the prompts to input your flat search criteria.

## Contribution
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

To contribute:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Antonio Evans - [@YourTwitter](https://twitter.com/YourTwitter) - email@example.com

Project Link: [https://github.com/antonioevans/FlatFinderAI](https://github.com/antonioevans/FlatFinderAI)
