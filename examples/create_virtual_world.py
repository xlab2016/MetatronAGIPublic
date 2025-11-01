#!/usr/bin/env python3
"""
Example: Create Virtual World from Idea
Demonstrates the core functionality of Metatron AGI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from metatron_agi import MetatronAGI


def main():
    """Main example demonstrating world creation from an idea."""

    print("=" * 80)
    print("METATRON AGI - VIRTUAL WORLD CREATION")
    print("Heuristic-based AGI without LLM integration")
    print("=" * 80)
    print()

    # The idea from the GitHub issue
    idea_russian = """
    Это мир высоких технологий где виртуальность интегрирована с реальностью.
    Можно придумать идею или мысль или попросить AGI воспроизвести сон или то что всплыло в сознании.
    AGI посредством нейроинтерфейса прочитает это. И создаст метамодель твоего описания.
    И начнет выстраивать вокруг него целый мир из концепций и форм.
    Затем он говорит готово ты надеваешь очки с нейро интерфейсом и целиком погружаешься в мир AGI.
    """

    # Alternative English idea for testing
    idea_english = """
    This is a high-tech world where virtuality is integrated with reality.
    You can come up with an idea or thought or ask AGI to reproduce a dream or something that came to mind.
    AGI will read this through a neural interface and create a meta-model of your description.
    It will begin to build an entire world of concepts and forms around it.
    Then it says it's ready, you put on glasses with a neural interface and completely immerse yourself in the AGI world.
    """

    # Initialize Metatron AGI
    print("Initializing Metatron AGI...")
    agi = MetatronAGI(
        language='russian',  # Change to 'english' for English processing
        dimensions=4,  # 4D conceptual space
        db_connection_string=None  # Will use environment variable or default
    )
    print("AGI initialized!\n")

    # Process the idea
    print("Processing your idea...")
    print(f"Input: {idea_russian[:100]}...\n")

    # Generate world (don't save to DB for this example)
    world = agi.process_idea(idea_russian, save_to_db=False)

    print("\n" + "=" * 80)
    print("WORLD GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print()

    # Display visualization
    visualization = agi.visualize_world(world, output_format='text')
    print(visualization)

    # Show some statistics
    print("\nDETAILED STATISTICS:")
    print(f"  - Space Type: {world['space']['name']}")
    print(f"  - Singularity Version: {world['singularity']['version']}")
    print(f"  - Concept Layers: {world['singularity']['layers_count']}")
    print(f"  - Dimensional Space: {world['metadata']['dimensions']}D")
    print()

    # Show concept graph structure
    print("CONCEPT HIERARCHY:")
    layers = {}
    for point in world['points']:
        layer = point['layer']
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(point['name'])

    for layer in sorted(layers.keys()):
        print(f"  Layer {layer}: {', '.join(layers[layer][:5])}")
        if len(layers[layer]) > 5:
            print(f"    ... and {len(layers[layer]) - 5} more")
    print()

    # Export to JSON file
    import json
    output_file = 'generated_world.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(world, f, indent=2, ensure_ascii=False)
    print(f"World exported to: {output_file}")
    print()

    # Optional: Interactive exploration
    response = input("Would you like to explore the world interactively? (y/n): ")
    if response.lower() == 'y':
        agi.explore_world_interactively(world)

    print("\nThank you for using Metatron AGI!")
    print("=" * 80)


if __name__ == '__main__':
    main()
