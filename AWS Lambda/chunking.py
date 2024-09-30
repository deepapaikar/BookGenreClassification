import string

# Predefined set of English stopwords
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been',
    'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'could', 'did', 'do', 'does',
    'doing', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'has', 'have', 'having',
    'he', 'her', 'here', 'hers',
    'herself', 'him', 'himself', 'his', 'how',
    'i', 'if', 'in', 'into', 'is',
    'it', 'its', 'itself', 'let', 'me', 'more', 'most',
    'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on',
    'once', 'only', 'or', 'other', 'our', 'ours',
    'ourselves', 'out', 'over', 'own', 'same', 'she',
    'should', 'so', 'some', 'such', 'than', 'that',
    'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'these', 'they', 'this', 'those',
    'through', 'to', 'too', 'under', 'until', 'up',
    'very', 'was', 'we', 'were', 'what', 'when', 'where',
    'which', 'while', 'who', 'whom', 'why', 'with', 'would',
    'you', 'your', 'yours', 'yourself', 'yourselves'
}

def remove_html_tags(text):
    """
    Removes HTML tags from the text by ignoring characters between '<' and '>'.
    """
    result = []
    inside_tag = False
    for char in text:
        if char == '<':
            inside_tag = True
            continue
        elif char == '>':
            inside_tag = False
            continue
        if not inside_tag:
            result.append(char)
    return ''.join(result)

def remove_punctuation(text):
    """
    Removes punctuation from the text by replacing them with spaces.
    """
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(translator)

def simple_lemmatize(word):
    """
    A very basic lemmatizer that removes common suffixes.
    Note: This is a simplistic implementation and not as robust as nltk's WordNetLemmatizer.
    """
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

def simple_stem(word):
    """
    A very basic stemmer that removes common suffixes.
    Note: This is a simplistic implementation and not as robust as nltk's SnowballStemmer.
    """
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

def clean_text(text):
    """
    Cleans the input text by performing the following:
    - Converts to lowercase
    - Removes HTML tags
    - Removes punctuation
    - Removes newlines
    - Removes stopwords and words with length <= 3
    - Removes single characters
    - Removes extra spaces
    - Performs simple lemmatization and stemming
    """
    # Convert to lowercase
    text = text.lower()

    # Remove HTML tags
    text = remove_html_tags(text)

    # Remove punctuation
    text = remove_punctuation(text)

    # Remove newlines
    text = text.replace('\n', ' ')

    # Split into words
    words = text.split()

    # Remove stopwords and words with length <=3
    filtered_words = [word for word in words if word not in STOPWORDS and len(word) > 3]

    # Perform simple lemmatization and stemming
    processed_words = [simple_stem(simple_lemmatize(word)) for word in filtered_words]

    # Remove any residual single characters and join back into string
    final_words = [word for word in processed_words if len(word) > 1]
    clean_text = ' '.join(final_words)

    # Remove extra spaces
    clean_text = ' '.join(clean_text.split())

    return clean_text

def split_text_into_chunks(text, chunk_size=2040, chunk_overlap=10):
    """
    Splits the text into chunks of specified size with a defined overlap.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap  # Move back by chunk_overlap for the next chunk

    return chunks

def split_and_reduce_chunks(text, chunk_size=2040, chunk_overlap=10):
    """
    Cleans the text, splits it into chunks, and reduces the number of chunks
    to a maximum if necessary by focusing on the middle portion of the text.
    """
    # Clean the text
    cleaned_text = clean_text(text)

    # Remove duplicate words while preserving order
    seen = set()
    unique_words = []
    for word in cleaned_text.split():
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    final_text = ' '.join(unique_words)

    # Determine maximum number of chunks based on the length of final_text
    max_chunks = max(1, len(final_text) // chunk_size)

    # Split the text into chunks
    chunks = split_text_into_chunks(final_text, chunk_size, chunk_overlap)

    # Reduce the number of chunks if necessary
    if len(chunks) > max_chunks:
        # Calculate the start index to get the middle portion of the chunks
        excess_chunks = len(chunks) - max_chunks
        start_index = excess_chunks // 2
        end_index = start_index + max_chunks
        chunks = chunks[start_index:end_index]

    return chunks
