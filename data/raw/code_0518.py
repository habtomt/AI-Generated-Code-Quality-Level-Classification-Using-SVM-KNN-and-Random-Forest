"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_004.txt
Run      : 1
"""

# Import necessary libraries
from transformers import pipeline

# Function to summarize text document
def summarize_text(document, max_length=150, min_length=25):
    """
    Generate a summary of a text document using a transformers model.

    Args:
        document (str): The text document to be summarized.
        max_length (int, optional): The maximum length of the summary. Defaults to 150.
        min_length (int, optional): The minimum length of the summary. Defaults to 25.

    Returns:
        str: The generated summary.
    """

    # Initialize the summarization pipeline
    try:
        # Attempt to load the summarization pipeline
        summarizer = pipeline("summarization")
    except Exception as e:
        # If there's an error loading the pipeline, print the error and exit
        print(f"Failed to load summarization pipeline: {e}")
        return None

    # Generate summary
    try:
        # Attempt to generate the summary
        summary = summarizer(document, max_length=max_length, min_length=min_length, do_sample=False)
    except Exception as e:
        # If there's an error generating the summary, print the error and exit
        print(f"Failed to generate summary: {e}")
        return None

    # Return the summary text
    return summary[0]['summary_text']

if __name__ == "__main__":
    # Example long text document
    text_document = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, 
    information engineering, and artificial intelligence concerned with the 
    interactions between computers and human (natural) languages, in particular how to 
    program computers to process and analyze large amounts of natural language data.
    The result is a computer capable of "understanding" the contents of documents, 
    including the contextual nuances of the language within them. The technology can 
    then accurately extract information and insights contained in the documents as 
    well as categorize and organize the documents themselves.
    """

    # Generate a summary
    summary = summarize_text(text_document)

    # Print the summary
    print("Summary:")
    print(summary)