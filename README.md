<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
 
</head>
<body>

<h1>🌍 Smart Travel Planner</h1>

<p>This repository contains a modularized Python application that helps users plan their trips. It leverages AI (via OpenAI's LLM) to generate itineraries, resolves city codes, checks weather conditions, and estimates trip costs including hotel prices and activity entrance fees. The application provides a user-friendly interface powered by Streamlit.</p>

<h2>✨ Features</h2>
<ul>
  <li><strong>AI-Powered Itinerary Generation:</strong> Creates a day-by-day itinerary for a given location and dates.</li>
  <li><strong>Intelligent City Code Resolution:</strong> Automatically converts natural city names to IATA codes using an LLM for seamless integration with travel APIs.</li>
  <li><strong>Weather Checking:</strong> Integrates with a search API (Tavily) to check weather conditions and suggests alternate dates if rain is detected.</li>
  <li><strong>Hotel Search & Pricing:</strong> Fetches hotel offers and prices using the Amadeus API.</li>
  <li><strong>Cost Estimation:</strong> Calculates estimated total costs including activity entrance fees and hotel expenses.</li>
  <li><strong>Modular Design:</strong> Code is structured into logical modules for better maintainability and reusability.</li>
  <li><strong>Streamlit UI:</strong> Provides an interactive web interface for easy input and display of trip plans.</li>
</ul>
<h2>📸 Preview</h2>
![image](https://github.com/user-attachments/assets/c940bd64-2851-452d-b371-dacbe65c4b8e)




<h2>📁 Project Structure</h2>
<ul>
  <li><strong>config.py:</strong> Handles loading environment variables (API keys) to keep sensitive information separate.</li>
  <li><strong>city_resolver.py:</strong> Contains the <code>CityCodeResolver</code> class to resolve city names to IATA codes and cache results.</li>
  <li><strong>hotel_search.py:</strong> Implements the <code>SmartHotelSearch</code> class and <code>parse_hotel_offers</code> function.</li>
  <li><strong>tools.py:</strong> Defines all the <code>@tool</code>-decorated LangGraph functions used in the workflow.</li>
  <li><strong>graph.py:</strong> Sets up the LangGraph workflow with nodes, edges, and <code>TravelState</code>.</li>
  <li><strong>main.py:</strong> The core backend logic that integrates and runs the travel planning workflow.</li>
  <li><strong>app.py:</strong> Streamlit app providing the UI for user inputs and output display.</li>
</ul>

<h2>⚙️ Setup</h2>

<ol>
  <li><strong>Clone the Repository</strong>
    <pre><code>git clone &lt;your-repository-url&gt;
cd smart-travel-planner</code></pre>
  </li>
  <li><strong>Install Dependencies</strong><br>
    It's recommended to use a virtual environment.
    <pre><code>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt</code></pre>
    If you don't have a <code>requirements.txt</code> file:
    <pre><code>pip install requests pandas openai langchain langchain-core langgraph python-dotenv streamlit tavily-python</code></pre>
  </li>
  <li><strong>Set Up Environment Variables</strong>
    <p>Create a <code>.env</code> file in the root directory with the following content:</p>
    <pre><code>AMADEUS_CLIENT_ID="YOUR_AMADEUS_CLIENT_ID"
AMADEUS_CLIENT_SECRET="YOUR_AMADEUS_CLIENT_SECRET"
OPENAI_API="YOUR_OPENAI_API_KEY"
TAVILY_API_KEY="YOUR_TAVILY_API_KEY"</code></pre>
    <p><em>⚠️ Do not commit your .env file to version control.</em></p>
  </li>
</ol>

<h2>🚀 How to Run</h2>
<p>After setup, run the application with:</p>
<pre><code>streamlit run app.py</code></pre>
<p>The app will open in your browser (usually at <a href="http://localhost:8501">http://localhost:8501</a>).</p>
<img width="834" alt="image" src="https://github.com/user-attachments/assets/de2c6d72-a87b-4701-8983-45e5b35726dc" />

<h2>🧭 Usage</h2>
<ol>
  <li><strong>Input Details:</strong> Enter the destination city and travel dates.</li>
  <li><strong>Plan Trip:</strong> Click the <em>"Plan My Trip!"</em> button.</li>
  <li><strong>View Summary:</strong> Itinerary, hotel prices, weather, and total costs will be displayed.</li>
</ol>

<h2>🐛 Troubleshooting</h2>
<ul>
  <li><strong>TypeError: argument of type 'NoneType' is not iterable:</strong> Check that all functions return valid data, especially in <code>main.py</code> and <code>tools.py</code>.</li>
  <li><strong>API Key Issues:</strong> Ensure your keys are correctly set and not expired.</li>
  <li><strong>Check Console Logs:</strong> Use print/debug logs in terminal for detailed execution flow.</li>
  <li><strong>No Hotel Results:</strong> The Amadeus test API may have limitations on some dates/locations. Also, <code>max_results</code> in <code>hotel_search.py</code> is limited for stability.</li>
  <li><strong>Incorrect Fees or Itineraries:</strong> Adjust prompts in <code>build_itinerary_tool</code> or logic in <code>calculate_fees_tool</code> as needed.</li>
</ul>

</body>
</html>
