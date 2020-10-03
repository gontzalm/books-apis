#!/home/gontz/miniconda3/envs/ih/bin/python
import src.mainhelpers as mh


def main():
    """Main execution program."""
    # Parse arguments
    args = mh.parse_argumets()

    # Load dataset
    books = mh.load_books()
    
    # Potentially filter data
    if any([args.topic, args.min_count, args.min_rating]):
        books = mh.filter_books(books, args)

    # Sort data
    books = mh.sort_books(books, args)

    # Potentially perform aggregations
    if args.aggregate:
        books = mh.aggregate_books(books)

    # Display data
    print(books.head(args.list))


if __name__ == "__main__":
    main()
