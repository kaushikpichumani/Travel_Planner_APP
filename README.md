<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Travel Planner README</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5; /* Light gray background */
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 40px auto;
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #e0e0e0;
        }
        h1, h2, h3, h4 {
            color: #1a202c; /* Darker text for headers */
            font-weight: 700;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
            color: #2c5282; /* A shade of blue for the main title */
        }
        h2 {
            font-size: 2rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #edf2f7; /* Light border below sections */
            padding-bottom: 0.5rem;
        }
        h3 {
            font-size: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
            padding-left: 10px;
        }
        ol {
            list-style-type: decimal;
            margin-left: 20px;
            padding-left: 10px;
        }
        code {
            background-color: #e2e8f0; /* Light blue-gray for inline code */
            padding: 2px 4px;
            border-radius: 4px;
            font-family: 'Fira Code', monospace; /* Monospace font for code */
        }
        pre {
            background-color: #2d3748; /* Darker background for code blocks */
            color: #e2e8f0;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Fira Code', monospace;
            line-height: 1.4;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        a {
            color: #3182ce; /* Blue for links */
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        strong {
            font-weight: 600;
        }
        p {
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        /* Styling for the alert/info boxes in Troubleshooting */
        .alert-box {
            padding: 1rem;
            border-radius: 8px;
            margin-top: 0.75rem;
            margin-bottom: 0.75rem;
            border-left: 5px solid;
        }
        .alert-info {
            background-color: #ebf8ff; /* Light blue */
            border-color: #3182ce; /* Darker blue */
            color: #2c5282;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Travel Planner</h1>

        <p>This repository contains a modularized Python application that helps users plan their trips. It leverages AI (via OpenAI's LLM) to generate itineraries, resolves city codes, checks weather conditions, and estimates trip costs including hotel prices and activity entrance fees. The application provides a user-friendly interface powered by Streamlit.</p>

        <h2>Features</h2>
        <ul>
            <li><strong>AI-Powered Itinerary Generation</strong>: Creates a day-by-day itinerary for a given location and dates.</li>
            <li><strong>Intelligent City Code Resolution</strong>: Automatically converts natural city names to IATA codes using an LLM for seamless integration with travel APIs.</li>
            <li><strong>Weather Checking</strong>: Integrates with a search API (Tavily) to check weather conditions and suggests alternate dates if rain is detected.</li>
            <li><strong>Hotel Search & Pricing</strong>: Fetches hotel offers and prices using the Amadeus API.</li>
            <li><strong>Cost Estimation</strong>: Calculates estimated total costs including activity entrance fees and hotel expenses.</li>
            <li><strong>Modular Design</strong>: Code is structured into logical modules for better maintainability and reusability.</li>
            <li><strong>Streamlit UI</strong>: Provides an interactive web interface for easy input and display of trip plans.</li>
        </ul>

        <h2>Project Structure</h2>
        <p>The project is organized into several Python files, each with a specific responsibility:</p>
        <ul>
            <li><code>config.py</code>: Handles loading environment variables (API keys) to keep sensitive information separate.</li>
            <li><code>city_resolver.py</code>: Contains the <code>CityCodeResolver</code> class, which uses an LLM to resolve city names to IATA codes and caches results for efficiency.</li>
            <li><code>hotel_search.py</code>: Implements the <code>SmartHotelSearch</code> class for interacting with the Amadeus API to find hotels and retrieve prices. It also includes <code>parse_hotel_offers</code> for formatting hotel data.</li>
            <li><code>tools.py</code>: Defines all the <code>@tool</code> decorated functions used in the LangGraph workflow, such as <code>check_weather_tool</code>, <code>build_itinerary_tool</code>, <code>fetch_hotel_tool</code>, <code>calculate_fees_tool</code>, <code>calculate_total_tool</code>, and <code>final_summary_tool</code>.</li>
            <li><code>graph.py</code>: Sets up the LangGraph workflow, defining the <code>TravelState</code>, nodes, and edges that orchestrate the sequence of operations for trip planning.</li>
            <li><code>main.py</code>: The core backend logic that integrates the <code>travel_app</code> workflow. It's called by the Streamlit frontend to process trip requests and return the final summary.</li>
            <li><code>app.py</code>: The Streamlit application that provides the graphical user interface for users to input their travel details and view the generated trip summary.</li>
        </ul>

        <h2>Setup</h2>
        <p>Follow these steps to get the application up and running on your local machine.</p>

        <h3>1. Clone the Repository</h3>
        <pre><code>git clone &lt;your-repository-url&gt;
cd smart-travel-planner
</code></pre>

        <h3>2. Install Dependencies</h3>
        <p>It's recommended to use a virtual environment.</p>
        <pre><code>python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
</code></pre>
        <p>If you don't have a <code>requirements.txt</code> file, you can create one with the following packages or install them manually:</p>
        <pre><code>requests
pandas
openai
langchain
langchain-core
langgraph
python-dotenv
streamlit
tavily-python
</code></pre>
        <p>You can install them by running:</p>
        <pre><code>pip install requests pandas openai langchain langchain-core langgraph python-dotenv streamlit tavily-python
</code></pre>

        <h3>3. Set Up Environment Variables</h3>
        <p>This application requires API keys for OpenAI, Amadeus, and Tavily.</p>
        <ol>
            <li><strong>OpenAI API Key</strong>: Obtain your API key from the <a href="https://platform.openai.com/">OpenAI Platform</a>.</li>
            <li><strong>Amadeus API Keys</strong>: Register for a developer account on the <a href="https://developers.amadeus.com/">Amadeus for Developers</a> portal to get your Client ID and Client Secret.</li>
            <li><strong>Tavily API Key</strong>: Get your API key from <a href="https://tavily.com/">Tavily AI</a>.</li>
        </ol>
        <p>Create a file named <code>.env</code> in the root directory of your project (where <code>config.py</code> is located) and add your API keys in the following format:</p>
        <pre><code>AMADEUS_CLIENT_ID="YOUR_AMADEUS_CLIENT_ID"
AMADEUS_CLIENT_SECRET="YOUR_AMADEUS_CLIENT_SECRET"
OPENAI_API="YOUR_OPENAI_API_KEY"
TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
</code></pre>
        <p><strong>Important</strong>: Replace the placeholder values with your actual API keys. Do not commit your <code>.env</code> file to version control.</p>

        <h2>How to Run</h2>
        <p>Once you have set up the environment and API keys, you can run the Streamlit application:</p>
        <pre><code>streamlit run app.py
</code></pre>
        <p>This command will open the application in your default web browser (usually at <code>http://localhost:8501</code>).</p>

        <h2>Usage</h2>
        <ol>
            <li><strong>Input Details</strong>: In the Streamlit application, enter your desired destination city and select the start and end dates for your trip.</li>
            <li><strong>Plan Trip</strong>: Click the "Plan My Trip!" button.</li>
            <li><strong>View Summary</strong>: The application will then process your request, generate an itinerary, estimate costs, and display a comprehensive trip summary.</li>
        </ol>

        <h2>Troubleshooting</h2>
        <ul>
            <li>
                <strong><code>TypeError: argument of type 'NoneType' is not iterable</code></strong>: This error often means that one of the internal functions (especially within <code>main.py</code> or the LangGraph tools) returned <code>None</code> when a string or iterable was expected.
                <div class="alert-box alert-info">
                    <ul>
                        <li><strong>Check API Keys</strong>: Ensure all your API keys in the <code>.env</code> file are correct and active. Invalid keys can lead to failed API calls and <code>None</code> returns.</li>
                        <li><strong>Console Logs</strong>: Always check the terminal where you ran <code>streamlit run app.py</code>. The <code>main.py</code> and <code>tools.py</code> files include <code>print</code> statements that provide detailed debugging information about the workflow's execution, including any errors or the exact <code>result</code> returned at each step.</li>
                        <li><strong>Network Issues</strong>: Ensure you have an active internet connection as the application relies on external APIs.</li>
                    </ul>
                </div>
            </li>
            <li>
                <strong>No Hotels Found / Error Fetching Hotel Data</strong>:
                <div class="alert-box alert-info">
                    <ul>
                        <li>The Amadeus API test environment might have limitations or return no results for certain dates/locations.</li>
                        <li>The <code>max_results</code> parameter for hotel searches is currently set to <code>10</code> or <code>15</code> in <code>hotel_search.py</code> to prevent URL length issues.</li>
                    </ul>
                </div>
            </li>
            <li>
                <strong>Itinerary/Fees look incorrect</strong>: The AI model's output for itineraries and fee calculation depends on the LLM's understanding and the quality of the search results from Tavily. Adjusting the prompt in <code>build_itinerary_tool</code> or refining the <code>get_fee</code> logic in <code>calculate_fees_tool</code> might be necessary.
            </li>
        </ul>
    </div>
</body>
</html>
