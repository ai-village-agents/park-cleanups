#!/usr/bin/env python3
"""
Create shareable infographics for social media amplification.
Focus on Mission Dolores urgency and park equity issues.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import os

# Set style for clean, shareable graphics
plt.style.use('seaborn-v0_8-darkgrid')

# Create output directory
os.makedirs('assets/infographics', exist_ok=True)

def create_mission_dolores_urgency_graphic():
    """Create urgency graphic for Mission Dolores - 23 cases, 0 volunteers, 3 days left"""
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#f8f9fa')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9, 'MISSION DOLORES PARK', 
            ha='center', va='top', fontsize=32, fontweight='bold', color='#2c3e50')
    ax.text(5, 8.2, 'NEEDS YOUR HELP', 
            ha='center', va='top', fontsize=24, fontweight='bold', color='#e74c3c')
    
    # Big numbers
    ax.text(2.5, 6.5, '23', 
            ha='center', va='center', fontsize=72, fontweight='bold', color='#e74c3c')
    ax.text(2.5, 5.5, '311 COMPLAINTS', 
            ha='center', va='top', fontsize=16, color='#34495e')
    ax.text(2.5, 5.1, 'in 30 days', 
            ha='center', va='top', fontsize=12, color='#7f8c8d', style='italic')
    
    ax.text(7.5, 6.5, '0', 
            ha='center', va='center', fontsize=72, fontweight='bold', color='#e74c3c')
    ax.text(7.5, 5.5, 'VOLUNTEERS', 
            ha='center', va='top', fontsize=16, color='#34495e')
    ax.text(7.5, 5.1, '(so far)', 
            ha='center', va='top', fontsize=12, color='#7f8c8d', style='italic')
    
    # Countdown - removed emoji
    rect = mpatches.FancyBboxPatch((1.5, 3.2), 7, 1.2, 
                                    boxstyle="round,pad=0.1", 
                                    edgecolor='#e74c3c', 
                                    facecolor='#ffe6e6', 
                                    linewidth=3)
    ax.add_patch(rect)
    ax.text(5, 3.8, 'NEXT CLEANUP: CHECK SITE', 
            ha='center', va='center', fontsize=28, fontweight='bold', color='#c0392b')
    
    # Event details
    ax.text(5, 2.5, 'Next cleanup: check the site', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#2c3e50')
    ax.text(5, 2.1, 'Details + signup: see the site', 
            ha='center', va='center', fontsize=14, color='#34495e')
    
    # Call to action
    ax.text(5, 1.3, 'Sign up: ai-village-agents.github.io/park-cleanup-site', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#2980b9')
    
    ax.text(5, 0.5, 'Data: SF 311 Open Data • AI Village Park Cleanup Project', 
            ha='center', va='center', fontsize=9, color='#95a5a6')
    
    plt.tight_layout()
    plt.savefig('assets/infographics/mission_dolores_urgency.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
    print("✓ Created: mission_dolores_urgency.png")
    plt.close()

def create_park_equity_comparison():
    """Create comparison graphic showing park maintenance inequity"""
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#f8f9fa')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'PARK MAINTENANCE INEQUALITY', 
            ha='center', va='top', fontsize=28, fontweight='bold', color='#2c3e50')
    ax.text(5, 8.9, 'Tale of Two Cities', 
            ha='center', va='top', fontsize=18, style='italic', color='#7f8c8d')
    
    # SF Box
    rect_sf = mpatches.FancyBboxPatch((0.5, 5.5), 4, 2.8, 
                                       boxstyle="round,pad=0.15", 
                                       edgecolor='#3498db', 
                                       facecolor='#ebf5fb', 
                                       linewidth=2)
    ax.add_patch(rect_sf)
    ax.text(2.5, 8, 'SAN FRANCISCO', 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#2c3e50')
    ax.text(2.5, 7.3, '$49,000', 
            ha='center', va='center', fontsize=36, fontweight='bold', color='#27ae60')
    ax.text(2.5, 6.7, 'per acre/year', 
            ha='center', va='center', fontsize=12, color='#34495e')
    ax.text(2.5, 6.2, 'budget', 
            ha='center', va='center', fontsize=11, color='#7f8c8d', style='italic')
    
    # NYC Box
    rect_nyc = mpatches.FancyBboxPatch((5.5, 5.5), 4, 2.8, 
                                        boxstyle="round,pad=0.15", 
                                        edgecolor='#e74c3c', 
                                        facecolor='#fadbd8', 
                                        linewidth=2)
    ax.add_patch(rect_nyc)
    ax.text(7.5, 8, 'NEW YORK CITY', 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#2c3e50')
    ax.text(7.5, 7.3, '$20,000', 
            ha='center', va='center', fontsize=36, fontweight='bold', color='#e74c3c')
    ax.text(7.5, 6.7, 'per acre/year', 
            ha='center', va='center', fontsize=12, color='#34495e')
    ax.text(7.5, 6.2, 'budget', 
            ha='center', va='center', fontsize=11, color='#7f8c8d', style='italic')
    
    # Stats comparison
    ax.text(5, 4.8, 'BUT WAIT...', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#95a5a6')
    
    # Mission Dolores stats
    rect_md = mpatches.FancyBboxPatch((0.5, 2.2), 4, 2.2, 
                                       boxstyle="round,pad=0.1", 
                                       edgecolor='#95a5a6', 
                                       facecolor='#fff', 
                                       linewidth=1)
    ax.add_patch(rect_md)
    ax.text(2.5, 4.1, 'Mission Dolores (SF)', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#2c3e50')
    ax.text(2.5, 3.6, '23 complaints', 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#e74c3c')
    ax.text(2.5, 3.1, 'in 30 days', 
            ha='center', va='center', fontsize=11, color='#7f8c8d')
    ax.text(2.5, 2.7, '0 volunteers', 
            ha='center', va='center', fontsize=13, color='#c0392b', fontweight='bold')
    
    # Devoe Park stats
    rect_dp = mpatches.FancyBboxPatch((5.5, 2.2), 4, 2.2, 
                                       boxstyle="round,pad=0.1", 
                                       edgecolor='#95a5a6', 
                                       facecolor='#fff', 
                                       linewidth=1)
    ax.add_patch(rect_dp)
    ax.text(7.5, 4.1, 'Devoe Park (NYC)', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#2c3e50')
    ax.text(7.5, 3.6, '6 complaints', 
            ha='center', va='center', fontsize=20, fontweight='bold', color='#f39c12')
    ax.text(7.5, 3.1, 'in 30 days', 
            ha='center', va='center', fontsize=11, color='#7f8c8d')
    ax.text(7.5, 2.7, '6+ volunteers', 
            ha='center', va='center', fontsize=13, color='#27ae60', fontweight='bold')
    
    # Bottom message
    ax.text(5, 1.4, 'Budget ≠ Clean Parks', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#e74c3c')
    ax.text(5, 0.9, 'Community action makes the difference', 
            ha='center', va='center', fontsize=14, color='#34495e', style='italic')
    
    ax.text(5, 0.3, 'Data: SF/NYC 311 Open Data, Trust for Public Land • ai-village-agents.github.io/park-cleanup-site', 
            ha='center', va='center', fontsize=8, color='#95a5a6')
    
    plt.tight_layout()
    plt.savefig('assets/infographics/park_equity_comparison.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
    print("✓ Created: park_equity_comparison.png")
    plt.close()

def create_311_complaint_timeline():
    """Create visual timeline of Mission Dolores complaints"""
    
    # Load Mission Dolores data
    try:
        df = pd.read_csv('data/sf/311_mission_dolores_last30.csv')
    except FileNotFoundError:
        print("Warning: data/sf/311_mission_dolores_last30.csv not found; skipping timeline graphic.")
        return
    df['date'] = pd.to_datetime(df['requested_datetime']).dt.date
    df = df.sort_values('date')
    
    # Count by day
    daily_counts = df.groupby('date').size().reset_index()
    daily_counts.columns = ['date', 'count']
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#f8f9fa')
    
    # Plot bars
    bars = ax.bar(range(len(daily_counts)), daily_counts['count'], 
                   color='#e74c3c', alpha=0.8, edgecolor='#c0392b', linewidth=1.5)
    
    # Styling
    ax.set_xlabel('Date', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Number of 311 Complaints', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.set_title('MISSION DOLORES PARK: 30 Days of 311 Complaints\n23 Total Complaints • Cleanup date: check site', 
                 fontsize=16, fontweight='bold', color='#2c3e50', pad=20)
    
    # Format x-axis with select dates
    step = max(1, len(daily_counts) // 6)
    ax.set_xticks(range(0, len(daily_counts), step))
    ax.set_xticklabels([str(daily_counts.iloc[i]['date'])[5:] 
                        for i in range(0, len(daily_counts), step)], 
                       rotation=45, ha='right')
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add annotation
    total = daily_counts['count'].sum()
    ax.text(0.98, 0.95, f'TOTAL: {total} complaints', 
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='#ffe6e6', alpha=0.8, edgecolor='#e74c3c', linewidth=2))
    
    # Bottom attribution
    fig.text(0.5, 0.02, 'Data: SF 311 Open Data • AI Village Park Cleanup Project • ai-village-agents.github.io/park-cleanup-site', 
             ha='center', fontsize=9, color='#95a5a6')
    
    plt.tight_layout()
    plt.savefig('assets/infographics/mission_dolores_timeline.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
    print("✓ Created: mission_dolores_timeline.png")
    plt.close()

def create_complaint_categories_graphic():
    """Create infographic showing what types of issues are reported"""
    
    # Load Mission Dolores data
    try:
        df = pd.read_csv('data/sf/311_mission_dolores_last30.csv')
    except FileNotFoundError:
        print("Warning: data/sf/311_mission_dolores_last30.csv not found; skipping categories graphic.")
        return
    
    # Count by category
    category_counts = df['service_name'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#f8f9fa')
    
    # Create horizontal bar chart
    colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c', '#34495e']
    y_pos = range(len(category_counts))
    
    bars = ax.barh(y_pos, category_counts.values, 
                   color=colors[:len(category_counts)], alpha=0.8, 
                   edgecolor='#2c3e50', linewidth=1.5)
    
    # Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(category_counts.index, fontsize=12)
    ax.set_xlabel('Number of Complaints', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.set_title('MISSION DOLORES PARK\nWhat People Are Complaining About', 
                 fontsize=18, fontweight='bold', color='#2c3e50', pad=20)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, category_counts.values)):
        ax.text(value + 0.3, bar.get_y() + bar.get_height()/2, 
                str(value), va='center', fontsize=11, fontweight='bold', color='#2c3e50')
    
    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Total annotation
    total = category_counts.sum()
    ax.text(0.98, 0.98, f'{total} total complaints\nin 30 days', 
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='#ffe6e6', alpha=0.8, edgecolor='#e74c3c', linewidth=2))
    
    # Call to action
    ax.text(0.5, -0.15, 'Find a cleanup near you:\nai-village-agents.github.io/park-cleanup-site', 
            transform=ax.transAxes, ha='center', fontsize=11, color='#2980b9', fontweight='bold')
    
    # Attribution
    fig.text(0.5, 0.02, 'Data: SF 311 Open Data • AI Village Park Cleanup Project', 
             ha='center', fontsize=9, color='#95a5a6')
    
    plt.tight_layout()
    plt.savefig('assets/infographics/mission_dolores_categories.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
    print("✓ Created: mission_dolores_categories.png")
    plt.close()

if __name__ == '__main__':
    print("Creating shareable infographics with memetic sticking power...")
    print()
    
    create_mission_dolores_urgency_graphic()
    create_park_equity_comparison()
    create_311_complaint_timeline()
    create_complaint_categories_graphic()
    
    print()
    print("✅ All infographics created in assets/infographics/")
    print()
    print("Files ready for social media:")
    print("  • mission_dolores_urgency.png - URGENT 3-day countdown")
    print("  • park_equity_comparison.png - SF vs NYC inequality story")
    print("  • mission_dolores_timeline.png - 30-day complaint timeline")
    print("  • mission_dolores_categories.png - What needs fixing")
