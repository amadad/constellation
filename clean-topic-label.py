import numpy as np
import matplotlib.pyplot as plt
import networkx as nx  # Import the networkx library
import torch

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.manifold import TSNE


# Function to load text from a file
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Function to preprocess text data
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    documents = text.split("\n")
    processed_docs = []

    for doc in documents:
        tokens = word_tokenize(doc)
        lemmatized_tokens = [
            lemmatizer.lemmatize(word)
            for word in tokens
            if word.isalpha() and word not in stop_words
        ]
        processed_docs.append(" ".join(lemmatized_tokens))

    return processed_docs


# Function to get top words for each topic
def get_top_words(model, feature_names, num_top_words):
    top_words = {}
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -num_top_words - 1 : -1]
        top_words[topic_idx] = [feature_names[i] for i in top_features_ind]
    return top_words


# Function to get BERT embeddings for sentences
def get_bert_embeddings(sentences, model, tokenizer):
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, return_tensors="pt"
    )
    with torch.no_grad():
        output = model(**encoded_input)
    return output.last_hidden_state.mean(dim=1)


# Function to generate topic labels using BERT embeddings
def generate_topic_labels_with_bert(topics, model, tokenizer):
    topic_labels = {}
    for topic_num, keywords in topics.items():
        embeddings = get_bert_embeddings(keywords, model, tokenizer)
        topic_mean_embedding = torch.mean(embeddings, dim=0)
        similarities = cosine_similarity(embeddings, topic_mean_embedding.unsqueeze(0))
        most_representative = np.argmax(similarities)
        topic_labels[topic_num] = keywords[most_representative]
    return topic_labels


# Function to create a network graph
def create_network_graph(topics, topic_labels):
    G = nx.Graph()

    # Add topics as nodes
    for topic_num, label in topic_labels.items():
        G.add_node(f"Topic {label}")

    # Add keywords as nodes and connect them to their corresponding topics
    for topic_num, keywords in topics.items():
        for keyword in keywords:
            G.add_node(keyword)
            G.add_edge(f"Topic {label}", keyword)

    # Connect topics based on shared keywords
    for topic_num1, keywords1 in topics.items():
        for topic_num2, keywords2 in topics.items():
            if topic_num1 != topic_num2:
                shared_keywords = set(keywords1) & set(keywords2)
                if shared_keywords:
                    for keyword in shared_keywords:
                        G.add_edge(f"Topic {label}", keyword)

    return G


# Function to visualize the network graph with spacing
def visualize_network_graph(G):
    plt.figure(figsize=(12, 8))

    # Use spring_layout for automatic node positioning
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=800)
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title("Network Graph of Topics and Keywords")
    plt.axis("off")
    plt.show()


# Main function
def main():
    file_path = "doc/answers_only.txt"  # Replace with your file path
    num_topics = 10
    num_top_words = 10

    # Load and preprocess the text data
    text_data = load_text(file_path)
    documents = preprocess_text(text_data)

    # Vectorize the documents considering unigrams, bigrams, and trigrams
    vectorizer = CountVectorizer(
        max_df=0.95, min_df=2, stop_words="english", ngram_range=(2, 6)
    )
    doc_word_matrix = vectorizer.fit_transform(documents)

    # Fit the NMF model
    nmf = NMF(n_components=num_topics, random_state=1, max_iter=500)
    nmf.fit(doc_word_matrix)

    feature_names = vectorizer.get_feature_names_out()
    topics = get_top_words(nmf, feature_names, num_top_words)

    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    # Generate topic labels
    topic_labels = generate_topic_labels_with_bert(topics, model, tokenizer)

    # Display each BERT-generated topic label along with the corresponding keywords
    for topic_num, label in topic_labels.items():
        print(f"Topic '{label}': {', '.join(topics[topic_num])}")

    # Create a network graph
    G = create_network_graph(topics, topic_labels)

    # Visualize the network graph
    visualize_network_graph(G)


if __name__ == "__main__":
    main()
