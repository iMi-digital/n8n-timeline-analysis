# n8n Workflow Profiler

Analyzes n8n workflow executions with interactive visualizations and performance insights.

## Features

- **Interactive Plot Viewer**: Navigate between 5 visualization types with keyboard controls
- **Performance Analysis**: Total time, average time, execution count, success rate, and hierarchical timeline
- **Export Support**: Save plots as high-resolution PNG files

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

```bash
# Analyze a specific execution
python3 n8n-timings.py --execution-id 1000

# Export plots as PNG files
python3 n8n-timings.py --execution-id 1000 --export-png
```

**Controls**: <kbd>←</kbd>/<kbd>→</kbd> to navigate, <kbd>Q</kbd> to close

## Output

- **Console Summary**: Execution details and node statistics
- **Interactive Plots**: Total time, average time, execution count, success rate, and timeline view


![`1000_0_TotalTime.png`](plots/1000_0_TotalTime.png)

![`1000_1_AvgTime.png`](plots/1000_1_AvgTime.png)

![`1000_2_ExecutionCount.png`](plots/1000_2_ExecutionCount.png)

![`1000_3_SuccessRate.png`](plots/1000_3_SuccessRate.png)

![`1000_4_HierarchicalTimeline.png`](plots/1000_4_HierarchicalTimeline.png)