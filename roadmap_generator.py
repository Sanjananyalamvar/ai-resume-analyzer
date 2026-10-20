from urllib.parse import quote_plus

TOPICS = {
    'Python': ('Python fundamentals', 'https://docs.python.org/3/tutorial/'),
    'SQL': ('SQL queries and joins', 'https://sqlbolt.com/'),
    'Pandas': ('Data analysis with Pandas', 'https://pandas.pydata.org/docs/getting_started/'),
    'NumPy': ('Numerical computing with NumPy', 'https://numpy.org/learn/'),
    'Machine Learning': ('Machine learning fundamentals', 'https://scikit-learn.org/stable/getting_started.html'),
    'scikit-learn': ('Model training and evaluation', 'https://scikit-learn.org/stable/'),
    'Power BI': ('Power BI learning path', 'https://learn.microsoft.com/training/powerplatform/power-bi/'),
    'Docker': ('Docker getting started', 'https://docs.docker.com/get-started/'),
    'Git': ('Git book', 'https://git-scm.com/book/en/v2'),
    'JavaScript': ('JavaScript guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide'),
    'React': ('React learn', 'https://react.dev/learn'),
    'FastAPI': ('FastAPI tutorial', 'https://fastapi.tiangolo.com/tutorial/'),
    'Django': ('Django tutorial', 'https://docs.djangoproject.com/en/stable/intro/tutorial01/'),
    'PyTorch': ('PyTorch tutorials', 'https://pytorch.org/tutorials/'),
    'TensorFlow': ('TensorFlow tutorials', 'https://www.tensorflow.org/tutorials'),
}


def make_roadmap_with_links(missing):
    """One entry per missing skill, two skills per week.

    Every entry has: week, skill, topic, docs, video, url (same as docs) and task.
    """
    out = []
    for i, s in enumerate(missing or [], 1):
        s = str(s)
        topic, docs = TOPICS.get(s, (f'Learn {s} fundamentals',
                                     f'https://www.google.com/search?q={quote_plus(s + " official documentation")}'))
        video = f'https://www.youtube.com/results?search_query={quote_plus(s + " tutorial for beginners")}'
        out.append({'week': ((i - 1) // 2) + 1, 'skill': s, 'topic': topic, 'docs': docs, 'video': video,
                    'url': docs, 'task': f'Complete one beginner lesson and build a small example using {s}.'})
    return out
