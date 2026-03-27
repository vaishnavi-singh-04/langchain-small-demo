
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitterLlmPipeline:
    def __init__(self) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100
        )
    
    def text_split(self, text: str):
        return self.splitter.split_text(text=text)