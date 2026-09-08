# Frequently Asked Questions (FAQ)

### What is FortSight AI?
FortSight AI is a specialized Geographic Information System (GIS) combined with AI, designed specifically for analyzing and exploring the hill forts of Maharashtra. 

### Why do I need a DEM file?
Digital Elevation Models (DEM) are required to calculate the line of sight accurately. Without them, the system cannot determine if a mountain or hill is blocking the view between two points.

### Can I deploy this without Docker?
Yes. You can follow the [Installation Guide](INSTALLATION.md) to set up the environment natively on your OS. However, Docker is highly recommended for production to avoid dependency conflicts, particularly with geospatial libraries like GDAL.

### Does the Chatbot support languages other than Marathi and English?
Currently, the RAG embeddings and LLM prompts are optimized for English and Marathi historical contexts. Additional languages can be supported by updating the embedding models and prompts in the `ml/` directory.
