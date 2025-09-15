from langchain_community.document_loaders import TextLoader
test = TextLoader('notes.txt')
test.load()