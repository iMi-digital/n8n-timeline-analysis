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

## Examples

Export plots as high-resolution PNG files:

```bash
# Export with default 1920x1080 resolution
python3 n8n-timings.py --execution-id 1000 --export-png

# Export with custom resolution
python3 n8n-timings.py --execution-id 1000 --export-png --png-width 3500 --png-height 1500
```

**Output**: Files saved to `plots/` directory with format `{EXECUTIONID}_{INDEX}_{PlotName}.png`

- ![`1000_0_TotalTime.png`](plots/1000_0_TotalTime.png)
- ![`1000_1_AvgTime.png`](plots/1000_1_AvgTime.png)
- ![`1000_2_ExecutionCount.png`](plots/1000_2_ExecutionCount.png)
- ![`1000_3_SuccessRate.png`](plots/1000_3_SuccessRate.png)
- ![`1000_4_HierarchicalTimeline.png`](plots/1000_4_HierarchicalTimeline.png)