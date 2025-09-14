# n8n Looped Node Analyzer

Analyzes n8n workflow executions where nodes run multiple times, providing interactive visualizations and performance insights.

## Features

- **Interactive Plot Viewer**: Navigate between 5 visualization types with keyboard controls
- **Multiple Analysis Views**: Total time, average time, execution count, success rate, and hierarchical timeline
- **Performance Analysis**: Detailed statistics and execution summaries

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your n8n API credentials in the `.env` file:
```
N8N_API_KEY=your_api_key_here
N8N_BASE_URL=https://your-n8n-instance.com
```

## Usage

### Analyze a specific execution:
```bash
python3 n8n-timings.py --execution-id 1000
```

**Controls**: <kbd>←</kbd>/<kbd>→</kbd> to navigate, <kbd>Q</kbd> to close

## Output

**Console Summary**: Execution details, node statistics, and individual execution timestamps

**Interactive Plots**:
- Total execution time by node
- Average execution time by node  
- Execution count by node
- Success rate by node
- Hierarchical timeline view

![Screenshot](docs/screenshot.png)