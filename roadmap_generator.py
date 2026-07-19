"""
roadmap_generator.py
---------------------
Turns a list of missing skills into a simple, rule-based, week-by-week
learning roadmap. This is the "beginner approach" from the project brief
(no ML model, just a lookup table + even distribution across weeks).

To extend: swap `_suggestion_for` with a call to an LLM (see
ai_feedback.py) to generate richer, personalized suggestions -- keep the
weekly-grouping logic the same so the rest of the app doesn't change.
"""

import math

# A small, easily-extensible knowledge base of learning suggestions.
# Keys must be lowercase to match the normalized skill names.
LEARNING_RESOURCES = {
    "python": "Practice core Python: data structures, functions, and OOP basics.",
    "sql": "Practice SQL: joins, aggregations, subqueries, and window functions.",
    "excel": "Learn Excel: pivot tables, VLOOKUP/XLOOKUP, and charts.",
    "power bi": "Learn Power BI: connecting data sources, DAX basics, and dashboards.",
    "tableau": "Learn Tableau: building interactive dashboards and calculated fields.",
    "pandas": "Practice Pandas: dataframes, groupby, merging, and cleaning data.",
    "numpy": "Learn NumPy: arrays, broadcasting, and vectorized operations.",
    "machine learning": "Study the ML workflow: train/test split, evaluation metrics, overfitting.",
    "scikit-learn": "Build a few scikit-learn pipelines: preprocessing + a classifier/regressor.",
    "deep learning": "Learn deep learning basics: neural networks, backpropagation, activation functions.",
    "tensorflow": "Build a small image or text classifier using TensorFlow/Keras.",
    "pytorch": "Build a small neural network from scratch using PyTorch.",
    "keras": "Practice building and training models with the Keras Sequential API.",
    "cnn": "Learn Convolutional Neural Networks for image classification tasks.",
    "rnn": "Learn Recurrent Neural Networks / LSTMs for sequence data.",
    "transformers": "Learn Transformer architecture basics (attention, encoder/decoder).",
    "nlp": "Learn core NLP: tokenization, embeddings, and text classification.",
    "spacy": "Practice spaCy: tokenization, NER, and POS tagging pipelines.",
    "nltk": "Practice NLTK: tokenization, stemming, and basic text preprocessing.",
    "hugging face": "Explore the Hugging Face `transformers` library and pretrained models.",
    "llm": "Learn LLM fundamentals: prompting, embeddings, and evaluation.",
    "rag": "Learn Retrieval-Augmented Generation: vector stores + LLM prompting.",
    "sentence transformers": "Practice generating sentence embeddings for semantic search.",
    "opencv": "Practice OpenCV: image loading, filtering, and basic object detection.",
    "yolo": "Learn YOLO for real-time object detection.",
    "image processing": "Learn image processing basics: filtering, edge detection, transforms.",
    "aws": "Get familiar with core AWS services: S3, EC2, and IAM basics.",
    "azure": "Get familiar with core Azure services: Blob Storage and Azure ML.",
    "gcp": "Get familiar with core GCP services: Cloud Storage and Vertex AI.",
    "cloud deployment": "Deploy a small model or app to a cloud platform end-to-end.",
    "docker": "Learn Docker: images, containers, Dockerfile, and docker-compose.",
    "kubernetes": "Learn Kubernetes basics: pods, deployments, and services.",
    "git": "Practice Git: branching, commits, merges, and resolving conflicts.",
    "github": "Practice GitHub workflows: pull requests, issues, and Actions basics.",
    "ci/cd": "Learn CI/CD basics: automated testing and deployment pipelines.",
    "mlflow": "Learn MLflow for experiment tracking and model registry.",
    "fastapi": "Build a small REST API with FastAPI (routes, request/response models).",
    "linux": "Practice Linux command line basics: file system, permissions, processes.",
    "matplotlib": "Practice Matplotlib: line, bar, and scatter plots.",
    "plotly": "Practice Plotly: interactive charts and dashboards.",
    "html": "Learn HTML basics: structure, forms, and semantic tags.",
    "css": "Learn CSS basics: layout, flexbox/grid, and responsive design.",
    "react": "Build a small React app using components, props, and state.",
    "node.js": "Build a small backend service using Node.js and Express.",
    "rest api": "Learn REST API design: endpoints, status codes, and JSON payloads.",
    "streamlit": "Build a small interactive Streamlit app.",
    "flask": "Build a small REST API or web app using Flask.",
    "django": "Build a small web app using Django's models, views, and templates.",
}


def _suggestion_for(skill: str) -> str:
    return LEARNING_RESOURCES.get(
        skill.lower(),
        f"Learn the fundamentals of {skill} through official docs and a small hands-on project.",
    )


def generate_roadmap(missing_skills: list, weeks: int = 4) -> list:
    """
    Spreads missing skills evenly across `weeks` weeks.
    Returns: [{"week": 1, "topics": [{"skill": ..., "suggestion": ...}, ...]}, ...]
    """
    if not missing_skills:
        return []

    weeks = max(1, weeks)
    chunk_size = math.ceil(len(missing_skills) / weeks)

    roadmap = []
    for week_index in range(weeks):
        start = week_index * chunk_size
        chunk = missing_skills[start : start + chunk_size]
        if not chunk:
            break
        roadmap.append(
            {
                "week": week_index + 1,
                "topics": [
                    {"skill": skill, "suggestion": _suggestion_for(skill)} for skill in chunk
                ],
            }
        )
    return roadmap
