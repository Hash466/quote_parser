class Descriptors():
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class QuoteItem():
    tags = Descriptors()
    text = Descriptors()
    by = Descriptors()
    about = Descriptors()

    def __init__(
        self, tags: list[str], by: str, text: str, about_author: dict
    ) -> None:
        self.tags = tags
        self.text = text
        self.by = by
        self.about_author = about_author
    
    def __str__(self) -> str:
        return f"Цитата: {self.text}, автор: {self.by}"
    
    def fetch_object(self) -> dict:
        return {
            "text": self.text,
            "by": self.by,
            "about_author": self.about_author,
            "tags": self.tags
        }


class QuoteArr():
    arr = Descriptors()
    top_tags = Descriptors()

    def __init__(
        self, arr: list[str] = [], top_tags: list[str] = []
    ) -> None:
        self.arr = arr
        self.top_tags = top_tags
    
    def __str__(self) -> str:
        return (
            f"Количество цитат в массиве: {len(self.arr)} шт., топ "
            f"тегов: {self.top_tags}"
        )
    
    def get_len(self) -> int:
        return len(self.arr)
    
    def add_top_tag(self, tag: str) -> None:
        self.top_tags.append(tag)
    
    def add_quote(self, quote: QuoteItem) -> None:
        self.arr.append(quote.fetch_object())
    
    def fetch_object(self) -> dict:
        return {
            "quote_arr": self.arr,
            "top_tags": self.top_tags
        }
     

class Author():
    name = Descriptors()
    was_born = Descriptors()
    description = Descriptors()

    def __init__(
        self, name: str, was_born: str, description: str
    ) -> None:
        self.name = name
        self.was_born = was_born
        self.description = description
    
    def __str__(self) -> str:
        return f"Автор: {self.name}"
    
    def fetch_object(self) -> dict:
        return {
            "author_name": self.name,
            "author_was_born": self.was_born,
            "author_description": self.description
        }
