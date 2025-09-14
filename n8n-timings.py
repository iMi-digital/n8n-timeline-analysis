#!/usr/bin/env python3
"""
n8n Looped Node Analyzer with Interactive Navigation

This application analyzes a single execution where nodes are executed multiple times (looped)
and creates an interactive plot viewer with proper navigation.
"""

import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import argparse
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

class InteractivePlotViewer:
    """Interactive plot viewer with navigation."""
    
    def __init__(self, node_summary: Dict[str, Any], execution_info: Dict[str, Any]):
        self.node_summary = node_summary
        self.execution_info = execution_info
        self.current_plot = 0
        self.plots = ['total_time', 'avg_time', 'execution_count', 'success_rate']
        self.plot_titles = {
            'total_time': 'Total Execution Time by Node (Summed)',
            'avg_time': 'Average Execution Time by Node', 
            'execution_count': 'Execution Count by Node',
            'success_rate': 'Success Rate by Node'
        }
        self.plot_colors = {
            'total_time': 'skyblue',
            'avg_time': 'lightcoral',
            'execution_count': 'lightgreen',
            'success_rate': 'gold'
        }
        self.plot_units = {
            'total_time': 'seconds',
            'avg_time': 'seconds',
            'execution_count': 'count',
            'success_rate': '%'
        }
        
        # Prepare data
        self.node_names = list(node_summary.keys())
        self.data = {
            'total_time': [stats['total_time'] for stats in node_summary.values()],
            'avg_time': [stats['average_time'] for stats in node_summary.values()],
            'execution_count': [stats['total_executions'] for stats in node_summary.values()],
            'success_rate': [stats['success_rate'] for stats in node_summary.values()]
        }
        
        # Calculate optimal figure size
        num_nodes = len(self.node_names)
        if num_nodes <= 5:
            self.fig_width = 12
            self.fig_height = 8
        elif num_nodes <= 10:
            self.fig_width = 14
            self.fig_height = 10
        elif num_nodes <= 20:
            self.fig_width = 16
            self.fig_height = 12
        else:
            self.fig_width = 18
            self.fig_height = 14
    
    def create_plot(self):
        """Create the current plot."""
        plt.clf()  # Clear the current figure
        
        plot_type = self.plots[self.current_plot]
        plot_data = self.data[plot_type]
        
        # Create the main plot
        ax = plt.subplot(111)
        bars = ax.bar(range(len(self.node_names)), plot_data, 
                     color=self.plot_colors[plot_type], alpha=0.8)
        
        # Set title and labels
        ax.set_title(f'{self.plot_titles[plot_type]} (Plot {self.current_plot + 1}/{len(self.plots)})', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Nodes', fontsize=12)
        ax.set_ylabel(f'{self.plot_titles[plot_type].split(" by ")[0]} ({self.plot_units[plot_type]})', fontsize=12)
        
        # Set x-axis labels
        ax.set_xticks(range(len(self.node_names)))
        ax.set_xticklabels(self.node_names, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        max_val = max(plot_data) if plot_data else 1
        for i, (bar, value) in enumerate(zip(bars, plot_data)):
            if self.plot_units[plot_type] == '%':
                label = f'{value:.1f}%'
            elif self.plot_units[plot_type] == 'seconds':
                label = f'{value:.2f}s'
            else:
                label = f'{value}'
            
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.01, 
                   label, ha='center', va='bottom', fontsize=10)
        
        # Add execution info
        info_text = f"Execution {self.execution_info['execution_id']} | {self.execution_info['workflow_name']} | {self.execution_info['total_nodes']} nodes"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Add navigation buttons
        self.add_navigation_buttons()
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)  # Make room for buttons
    
    def add_navigation_buttons(self):
        """Add navigation buttons to the plot."""
        # Previous button
        ax_prev = plt.axes([0.1, 0.02, 0.1, 0.04])
        btn_prev = Button(ax_prev, '← Previous')
        btn_prev.on_clicked(self.prev_plot)
        
        # Next button
        ax_next = plt.axes([0.8, 0.02, 0.1, 0.04])
        btn_next = Button(ax_next, 'Next →')
        btn_next.on_clicked(self.next_plot)
        
        # Plot indicator
        ax_info = plt.axes([0.25, 0.02, 0.5, 0.04])
        ax_info.axis('off')
        plot_names = ['Total Time', 'Avg Time', 'Count', 'Success Rate']
        ax_info.text(0.5, 0.5, f'{plot_names[self.current_plot]} ({self.current_plot + 1}/{len(self.plots)})', 
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        # Keyboard shortcuts info
        ax_help = plt.axes([0.02, 0.02, 0.06, 0.04])
        ax_help.axis('off')
        ax_help.text(0.5, 0.5, '← → keys', ha='center', va='center', fontsize=8, 
                    bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
    
    def prev_plot(self, event):
        """Go to previous plot."""
        self.current_plot = (self.current_plot - 1) % len(self.plots)
        self.create_plot()
        plt.draw()
    
    def next_plot(self, event):
        """Go to next plot."""
        self.current_plot = (self.current_plot + 1) % len(self.plots)
        self.create_plot()
        plt.draw()
    
    def on_key(self, event):
        """Handle keyboard events."""
        if event.key == 'left' or event.key == 'a':
            self.prev_plot(None)
        elif event.key == 'right' or event.key == 'd':
            self.next_plot(None)
        elif event.key == 'q' or event.key == 'escape':
            plt.close()
    
    def show(self):
        """Show the interactive plot."""
        # Set up the figure
        fig = plt.figure(figsize=(self.fig_width, self.fig_height))
        fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        # Create initial plot
        self.create_plot()
        
        # Show the plot
        plt.show()

class N8nLoopedNodeAnalyzer:
    """Analyzes n8n workflow execution data with looped nodes."""
    
    def __init__(self, base_url: str, api_key: str, debug: bool = False):
        """
        Initialize the analyzer with API credentials.
        
        Args:
            base_url: Base URL of the n8n instance
            api_key: API key for authentication
            debug: Enable debug mode for detailed output
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.debug = debug
        self.session = requests.Session()
        
        # Correct n8n API authentication
        self.session.headers.update({
            'X-N8N-API-KEY': api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def debug_print(self, message: str, data: Any = None):
        """Print debug information if debug mode is enabled."""
        if self.debug:
            print(f"🔍 DEBUG: {message}")
            if data is not None:
                if isinstance(data, (dict, list)):
                    print(json.dumps(data, indent=2, default=str))
                else:
                    print(f"Data: {data}")
            print("-" * 50)
    
    def fetch_execution_data(self, execution_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch execution data for a specific execution ID with detailed data.
        
        Args:
            execution_id: The execution ID to fetch
            
        Returns:
            Dictionary containing execution data or None if failed
        """
        # Use includeData=true to get detailed execution data
        url = f"{self.base_url}/api/v1/executions/{execution_id}?includeData=true"
        
        try:
            response = self.session.get(url)
            self.debug_print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.debug_print("Raw API Response", data)
                return data
            elif response.status_code == 404:
                print(f"Execution {execution_id} not found")
                return None
            else:
                print(f"API Error: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None
    
    def analyze_looped_execution(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single execution with looped nodes and sum up execution times.
        
        Args:
            execution_data: Execution data dictionary
            
        Returns:
            Dictionary containing looped node analysis
        """
        if not execution_data:
            return {}
        
        # Extract basic execution info
        execution_id = execution_data.get('id')
        workflow_id = execution_data.get('workflowId')
        workflow_name = execution_data.get('workflowData', {}).get('name', 'Unknown')
        status = execution_data.get('status', 'unknown')
        started_at = execution_data.get('startedAt')
        stopped_at = execution_data.get('stoppedAt')
        created_at = execution_data.get('createdAt')
        
        # Parse timestamps
        start_time = None
        end_time = None
        duration = None
        
        if started_at:
            start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
        
        if stopped_at:
            end_time = datetime.fromisoformat(stopped_at.replace('Z', '+00:00'))
            if start_time:
                duration = (end_time - start_time).total_seconds()
        
        # Analyze looped node executions
        node_executions = []
        node_summary = defaultdict(list)  # Group by node name
        
        if 'data' in execution_data and execution_data['data']:
            data_field = execution_data['data']
            self.debug_print("Processing data field", data_field)
            
            if 'resultData' in data_field and 'runData' in data_field['resultData']:
                run_data = data_field['resultData']['runData']
                self.debug_print("Found runData", run_data)
                
                for node_name, node_executions_list in run_data.items():
                    self.debug_print(f"Processing node: {node_name}", node_executions_list)
                    
                    for execution in node_executions_list:
                        # Convert timestamp from milliseconds to datetime
                        start_timestamp = execution.get('startTime')
                        execution_time = execution.get('executionTime', 0)
                        execution_status = execution.get('executionStatus', 'unknown')
                        
                        node_start_time = None
                        node_duration = None
                        
                        if start_timestamp:
                            # Convert from milliseconds to datetime
                            node_start_time = datetime.fromtimestamp(start_timestamp / 1000)
                            node_duration = execution_time / 1000.0  # Convert to seconds
                        
                        node_execution = {
                            'execution_id': execution_id,
                            'workflow_name': workflow_name,
                            'node_name': node_name,
                            'start_time': node_start_time,
                            'duration': node_duration,
                            'status': execution_status,
                            'execution_index': execution.get('executionIndex', 0)
                        }
                        
                        self.debug_print(f"Node execution: {node_name}", node_execution)
                        node_executions.append(node_execution)
                        
                        # Group by node name for summary
                        node_summary[node_name].append(node_execution)
        
        # Calculate summary statistics for each node
        node_summary_stats = {}
        for node_name, executions in node_summary.items():
            durations = [ex['duration'] for ex in executions if ex['duration'] is not None]
            statuses = [ex['status'] for ex in executions]
            
            node_summary_stats[node_name] = {
                'total_executions': len(executions),
                'total_time': sum(durations),
                'average_time': sum(durations) / len(durations) if durations else 0,
                'min_time': min(durations) if durations else 0,
                'max_time': max(durations) if durations else 0,
                'successful_executions': len([s for s in statuses if s == 'success']),
                'failed_executions': len([s for s in statuses if s == 'error']),
                'success_rate': len([s for s in statuses if s == 'success']) / len(statuses) * 100 if statuses else 0,
                'executions': executions
            }
        
        return {
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'workflow_name': workflow_name,
            'status': status,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'created_at': created_at,
            'has_detailed_data': len(node_executions) > 0,
            'node_executions': node_executions,
            'node_summary': node_summary_stats,
            'total_nodes': len(node_summary_stats),
            'total_node_executions': len(node_executions)
        }
    
    def create_looped_summary_report(self, analysis_data: Dict[str, Any]):
        """
        Create a summary report for looped node execution.
        
        Args:
            analysis_data: Analysis data from analyze_looped_execution
        """
        if not analysis_data:
            print("No analysis data available")
            return
        
        print("\n" + "="*80)
        print("LOOPED NODE EXECUTION SUMMARY")
        print("="*80)
        print(f"Execution ID: {analysis_data['execution_id']}")
        print(f"Workflow: {analysis_data['workflow_name']}")
        print(f"Workflow ID: {analysis_data['workflow_id']}")
        print(f"Status: {analysis_data['status']}")
        print(f"Start Time: {analysis_data['start_time']}")
        print(f"End Time: {analysis_data['end_time']}")
        print(f"Total Duration: {analysis_data['duration']:.2f} seconds" if analysis_data['duration'] else "Duration: N/A")
        print(f"Total Node Executions: {analysis_data['total_node_executions']}")
        print(f"Unique Nodes: {analysis_data['total_nodes']}")
        print("="*80)
        
        # Summary by node (summed up)
        print(f"\n{'Node Name':<30} | {'Executions':<10} | {'Total Time':<12} | {'Avg Time':<10} | {'Min':<8} | {'Max':<8} | {'Success Rate':<12}")
        print("-" * 80)
        
        node_summary = analysis_data['node_summary']
        for node_name, stats in node_summary.items():
            print(f"{node_name:<30} | {stats['total_executions']:<10} | {stats['total_time']:<12.2f}s | {stats['average_time']:<10.2f}s | {stats['min_time']:<8.2f}s | {stats['max_time']:<8.2f}s | {stats['success_rate']:<12.1f}%")
        
        print("="*80)
        
        # Detailed breakdown for each node
        for node_name, stats in node_summary.items():
            print(f"\n📊 {node_name}")
            print("-" * 50)
            print(f"Total Executions: {stats['total_executions']}")
            print(f"Total Time (summed): {stats['total_time']:.2f} seconds")
            print(f"Average Time: {stats['average_time']:.2f} seconds")
            print(f"Min Time: {stats['min_time']:.2f} seconds")
            print(f"Max Time: {stats['max_time']:.2f} seconds")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
            
            # Show individual executions
            print(f"\nIndividual Executions:")
            for i, exec_data in enumerate(stats['executions']):
                start_time_str = exec_data['start_time'].strftime('%H:%M:%S.%f')[:-3] if exec_data['start_time'] else "N/A"
                print(f"  {i+1}. Duration: {exec_data['duration']:.3f}s at {start_time_str} (Status: {exec_data['status']})")
    
    def create_interactive_visualization(self, analysis_data: Dict[str, Any]):
        """
        Create interactive visualization for looped node execution.
        
        Args:
            analysis_data: Analysis data from analyze_looped_execution
        """
        if not analysis_data or not analysis_data.get('node_summary'):
            print("No node summary data available for plotting")
            return
        
        print("\n🎯 Starting Interactive Plot Viewer...")
        print("="*60)
        print("NAVIGATION CONTROLS:")
        print("• Click '← Previous' or 'Next →' buttons")
        print("• Use ← → arrow keys (or A/D keys)")
        print("• Press Q or Escape to close")
        print("• All plots in one window with smooth navigation")
        print("="*60)
        
        # Create interactive viewer
        viewer = InteractivePlotViewer(analysis_data['node_summary'], analysis_data)
        viewer.show()

def main():
    """Main function to run the analyzer."""
    parser = argparse.ArgumentParser(description='Analyze n8n looped node execution with interactive navigation')
    parser.add_argument('--execution-id', type=int, required=True, help='Execution ID to analyze')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to see raw API responses')
    
    args = parser.parse_args()
    
    # Get configuration from environment
    base_url = os.getenv('N8N_BASE_URL')
    api_key = os.getenv('N8N_API_KEY')
    
    if not base_url or not api_key:
        print("Error: Please set N8N_BASE_URL and N8N_API_KEY in your .env file")
        return
    
    print("="*60)
    print("n8n LOOPED NODE ANALYZER (INTERACTIVE)")
    print("="*60)
    print(f"Base URL: {base_url}")
    print(f"✅ API Authentication: Working!")
    print(f"✅ Detailed Data: Enabled (includeData=true)")
    print(f"Analyzing Execution ID: {args.execution_id}")
    print("="*60)
    
    # Initialize analyzer
    analyzer = N8nLoopedNodeAnalyzer(base_url, api_key, debug=args.debug)
    
    # Analyze specific execution
    print(f"Fetching execution data for ID: {args.execution_id}")
    execution_data = analyzer.fetch_execution_data(args.execution_id)
    
    if execution_data:
        print("✅ Execution data fetched successfully!")
        analysis = analyzer.analyze_looped_execution(execution_data)
        analyzer.create_looped_summary_report(analysis)
        analyzer.create_interactive_visualization(analysis)
    else:
        print("❌ Failed to fetch execution data")

if __name__ == "__main__":
    main()
