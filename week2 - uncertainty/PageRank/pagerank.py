import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = dict.fromkeys(corpus)
    probability_of_link_being_chosen_at_random = (1 - damping_factor) / len(corpus)
    for link in corpus:
        if link in corpus[page]:
            distribution[link] = (
                1 / len(corpus[page]) * damping_factor
            ) + probability_of_link_being_chosen_at_random
        else:
            distribution[link] = probability_of_link_being_chosen_at_random
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_count = {key: 0 for key in corpus}
    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        page_count[page] += 1
        distribution = transition_model(corpus, page, damping_factor)
        page = random.choices(
            list(distribution.keys()), weights=distribution.values(), k=1
        )[0]
    return {key: value / n for key, value in page_count.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {key: 1 / len(corpus) for key in corpus}
    repeat = True
    while repeat:
        new_rank = dict()
        for page in corpus:
            sum = 0
            for link_to_page in corpus:
                if page in corpus[link_to_page]:
                    sum += rank[link_to_page] / len(corpus[link_to_page])
                elif not corpus[link_to_page]:
                    sum += rank[link_to_page] / len(corpus)
            new_rank[page] = ((1 - damping_factor) / len(corpus)) + (
                damping_factor * sum
            )
        repeat = False
        for page in rank:
            if abs(new_rank[page] - rank[page]) >= 0.001:
                repeat = True
                break
        rank = new_rank
    return rank


if __name__ == "__main__":
    main()
