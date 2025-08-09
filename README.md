# 🧪 Test Data Creator - Phase 2 (LangGraph)

An intelligent test data generation tool that creates realistic e-commerce data using AI and stores it in a SQLite database. Built with LangGraph for robust workflow management and Streamlit for an intuitive user interface.

## 🌟 Features

### Core Capabilities
- **AI-Powered Data Generation**: Uses OpenAI GPT models to create realistic e-commerce order data
- **LangGraph Workflow**: Robust state management with automated data processing pipeline
- **SQLite Integration**: Automatic database storage with table management
- **Interactive UI**: Clean Streamlit interface for easy data generation
- **JSON Validation**: Ensures generated data meets schema requirements

### Data Types Supported
- **E-commerce Orders**: Customer orders with products, pricing, and location data
- **Indian Market Focus**: Includes Indian states, cities, and local product names
- **Realistic Patterns**: AI generates contextually appropriate data relationships

## 📊 Generated Data Schema

The application generates e-commerce order data with the following structure:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `customer_id` | String | Unique customer identifier | "IND1001" |
| `order_id` | String | Unique order identifier | "ORD1001" |
| `product_name` | String | Name of purchased product | "Kurta" |
| `category` | String | Product category | "Clothing" |
| `price` | Number | Product price in INR | 1200 |
| `quantity` | Number | Number of items ordered | 2 |
| `date` | String | Order date (YYYY-MM-DD) | "2024-03-08" |
| `state` | String | Customer state | "Maharashtra" |
| `city` | String | Customer city | "Mumbai" |
| `payment_method` | String | Payment type | "Credit Card" |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (paid service)

### Quick Setup
```bash
# 1. Install dependencies
pip install streamlit langgraph pandas sqlalchemy python-dotenv langchain-openai

# 2. Create environment file
touch .env

# 3. Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_actual_openai_key_here" > .env
```

### Detailed Installation
```bash
# Create project directory
mkdir test-data-creator
cd test-data-creator

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Requirements.txt
```txt
streamlit>=1.28.0
langgraph>=0.0.30
pandas>=2.0.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
langchain-openai>=0.1.0
langchain>=0.1.0
```

## 🔑 API Key Setup

### Getting OpenAI API Key
1. **Visit**: [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. **Sign in** or create an account
3. **Add billing information** (credit card required)
4. **Create new secret key**
5. **Copy the key** (starts with `sk-proj-` or `sk-`)

### Environment Configuration
Create a `.env` file in your project directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your_actual_openai_api_key_here

# Optional: Database configuration
DB_PATH=testdata.db
```

**⚠️ Important**: Never commit your `.env` file to version control!

Add to `.gitignore`:
```gitignore
.env
*.db
__pycache__/
```

## 🚀 Running the Application

### Local Development
```bash
# Run the Streamlit application
streamlit run test_data_creator.py
```

The application will open at `http://localhost:8501`

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "test_data_creator.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t test-data-creator .
docker run -p 8501:8501 --env-file .env test-data-creator
```

## 📱 How to Use

### 1. **Start the Application**
```bash
streamlit run test_data_creator.py
```

### 2. **Generate Data**
1. **Enter a request** in the text input (e.g., "Generate 10 orders for March 2024")
2. **Click "Generate & Store"**
3. **View generated data** in the dataframe display
4. **Data automatically stored** in SQLite database

### 3. **Monitor Database**
- **View existing tables** in the "Existing Tables in DB" section
- **Each generation** creates a new table (`table_1`, `table_2`, etc.)
- **Access database** directly at `testdata.db`

### Example Prompts
```
"Generate 10 orders for March 2024"
"Create data for electronics sales in Mumbai"
"Generate clothing orders from Delhi customers"
"Create orders with credit card payments only"
"Generate data for premium products above ₹5000"
```

## 🏗️ Architecture

### LangGraph Workflow
```mermaid
graph TD
    A[User Input] --> B[Synthesize Node]
    B --> C[LLM Processing]
    C --> D[JSON Validation]
    D --> E[Store Node]
    E --> F[SQLite Database]
    F --> G[Success Confirmation]
```

### Core Components

#### 1. **State Management**
```python
class AppState(TypedDict):
    messages: List[str]          # User input history
    generated_data: List[Dict]   # Generated JSON data
```

#### 2. **Workflow Nodes**
- **synthesize_data**: Calls OpenAI to generate realistic data
- **manage_db**: Stores generated data in SQLite with automatic table creation

#### 3. **Data Pipeline**
```
User Prompt → LLM Generation → JSON Parsing → Database Storage → UI Display
```

### Database Schema
- **Automatic table creation**: Each generation creates a new table
- **SQLite storage**: Local database file (`testdata.db`)
- **Pandas integration**: Easy data manipulation and display

## ⚙️ Configuration

### LLM Configuration
Modify the LLM settings in the code:
```python
llm = ChatOpenAI(
    model="gpt-4.1-nano",     # Model selection
    temperature=0.2,          # Creativity level (0.0-1.0)
    max_tokens=1000,          # Response length limit
    top_p=1.0                # Nucleus sampling
)
```

### System Prompt Customization
Modify the `system_prompt` to generate different data types:
```python
system_prompt = """
You are a data generator. Generate realistic [YOUR_DATA_TYPE] in JSON format.
Return ONLY a JSON array with objects containing:
[YOUR_FIELDS_HERE]

Generate exactly [NUMBER] records.
"""
```

### Database Configuration
```python
# Change database type
engine = create_engine("postgresql://user:pass@localhost/db")  # PostgreSQL
engine = create_engine("mysql://user:pass@localhost/db")       # MySQL
engine = create_engine(f"sqlite:///{DB_PATH}")                # SQLite (default)
```

## 🎯 Use Cases

### Software Testing
- **Load testing**: Generate large datasets for performance testing
- **Feature testing**: Create specific data scenarios
- **Edge case testing**: Generate boundary condition data

### Development
- **Mock data**: Populate development databases
- **Demo data**: Create realistic data for presentations
- **Prototype data**: Quickly generate data for proof-of-concepts

### Data Science
- **Synthetic datasets**: Create training data for ML models
- **Data augmentation**: Expand existing datasets
- **A/B testing**: Generate control datasets

### Business Analysis
- **Market research**: Generate sample customer data
- **Sales forecasting**: Create historical data patterns
- **Regional analysis**: Generate location-specific data

## 📈 Advanced Usage

### Custom Data Types
Modify the system prompt for different data types:

#### Financial Data
```python
system_prompt = """
Generate realistic financial transaction data:
transaction_id, account_number, amount, transaction_type, date, merchant, category
"""
```

#### User Profiles
```python
system_prompt = """
Generate realistic user profile data:
user_id, name, email, age, location, preferences, signup_date, subscription_type
"""
```

#### Inventory Data
```python
system_prompt = """
Generate realistic inventory data:
sku, product_name, category, stock_quantity, warehouse_location, supplier, cost_price
"""
```

### Batch Processing
```python
def generate_large_dataset(num_batches=10, records_per_batch=10):
    """Generate large datasets in batches"""
    all_data = []
    
    for i in range(num_batches):
        inputs = {"messages": [f"Generate batch {i+1}"], "generated_data": []}
        output = compiled_graph.invoke(inputs)
        all_data.extend(output.get("generated_data", []))
        
        # Progress tracking
        st.progress((i + 1) / num_batches)
    
    return all_data
```

### Data Export Options
```python
def export_data(table_name, format="csv"):
    """Export data in various formats"""
    df = pd.read_sql_table(table_name, engine)
    
    if format == "csv":
        return df.to_csv(index=False)
    elif format == "json":
        return df.to_json(orient="records", indent=2)
    elif format == "excel":
        return df.to_excel(index=False)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **OpenAI Authentication Error**
```
Error code: 401 - Invalid API key
```
**Solution**:
- Check your `.env` file has real API key (not placeholder)
- Verify key starts with `sk-proj-` or `sk-`
- Test key at [OpenAI Playground](https://platform.openai.com/playground)

#### 2. **JSON Parsing Error**
```
AI did not return valid JSON structured data
```
**Solutions**:
- Adjust `temperature` to 0.1 for more consistent JSON
- Modify system prompt for clearer JSON requirements
- Add JSON validation examples to prompt

#### 3. **Database Connection Error**
```
SQLAlchemy connection failed
```
**Solutions**:
- Check file permissions for SQLite database
- Ensure directory is writable
- Verify SQLAlchemy installation

#### 4. **Model Not Found Error**
```
Model gpt-4.1-nano not found
```
**Solution**:
Update to available model:
```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)  # or gpt-3.5-turbo
```

### Debug Mode
Enable debugging by adding:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Test LLM connection
def test_llm():
    try:
        response = llm([HumanMessage(content="Hello")])
        print("✅ LLM connection successful")
        return True
    except Exception as e:
        print(f"❌ LLM connection failed: {e}")
        return False
```

## 📊 Database Management

### View Generated Data
```python
# Read specific table
def view_table(table_name):
    df = pd.read_sql_table(table_name, engine)
    return df

# List all tables
def list_tables():
    inspector = inspect(engine)
    return inspector.get_table_names()

# Get table statistics
def table_stats(table_name):
    df = pd.read_sql_table(table_name, engine)
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage": df.memory_usage(deep=True).sum()
    }
```

### Data Quality Checks
```python
def validate_data(df):
    """Validate generated data quality"""
    issues = []
    
    # Check for missing values
    if df.isnull().sum().sum() > 0:
        issues.append("Contains null values")
    
    # Check price ranges
    if df['price'].min() < 0:
        issues.append("Contains negative prices")
    
    # Check date format
    try:
        pd.to_datetime(df['date'])
    except:
        issues.append("Invalid date format")
    
    return issues
```

### Database Cleanup
```python
def cleanup_database():
    """Remove old tables"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    # Keep only last 5 tables
    if len(tables) > 5:
        old_tables = tables[:-5]
        for table in old_tables:
            engine.execute(f"DROP TABLE {table}")
```

## 🚀 Deployment

### Local Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn (more robust than streamlit run)
streamlit run test_data_creator.py --server.port 8501
```

### Cloud Deployment

#### Streamlit Community Cloud
1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy**: Visit [Streamlit Community Cloud](https://share.streamlit.io/)
3. **Add secrets**: Include `OPENAI_API_KEY` in app secrets

#### Railway/Render
```yaml
# render.yaml
services:
  - type: web
    name: test-data-creator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run test_data_creator.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

### Environment Variables for Production
```env
# Production configuration
OPENAI_API_KEY=your_production_key
DB_PATH=production_testdata.db
ENVIRONMENT=production
LOG_LEVEL=INFO
```
