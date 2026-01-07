#!/usr/bin/env python3
"""Main script for generating flip books."""

import argparse
from flipbook.generator import FlipBookGenerator
from flipbook.formatter import FlipBookFormatter


def main():
    """Main entry point for the flip book generator."""
    parser = argparse.ArgumentParser(
        description="Generate children's flip book sentences"
    )
    parser.add_argument(
        "-n", "--num-pages",
        type=int,
        default=10,
        help="Number of pages to generate (default: 10)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file name (prints to console if not specified)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["print", "list"],
        default="print",
        help="Output format: 'print' for flip book layout, 'list' for simple list"
    )
    parser.add_argument(
        "--show-stats",
        action="store_true",
        help="Show statistics about possible combinations"
    )
    
    args = parser.parse_args()
    
    # Initialize generator and formatter
    generator = FlipBookGenerator()
    formatter = FlipBookFormatter(generator)
    
    # Show statistics if requested
    if args.show_stats:
        total = generator.get_total_combinations()
        print(f"\n📊 Flip Book Statistics:")
        print(f"   Subjects: {len(generator.nouns)}")
        print(f"   Verbs: {len(generator.verbs)}")
        print(f"   Objects: {len(generator.objects)}")
        print(f"   Total possible combinations: {total:,}\n")
    
    # Generate sentences
    print(f"🎨 Generating {args.num_pages} flip book pages...")
    sentences = generator.generate_book(args.num_pages)
    
    # Format and output
    if args.output:
        formatter.save_to_file(sentences, args.output, args.format)
        print(f"✅ Saved to {args.output}")
    else:
        if args.format == "print":
            print(formatter.format_for_print(sentences))
        else:
            print(formatter.format_as_list(sentences))
    
    print("\n💡 Tip: Cut each page along the lines to create your flip book!")


if __name__ == "__main__":
    main()
