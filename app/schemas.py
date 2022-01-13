from .models import Book


BookIn = Book.get_pydantic(exclude={"pk", "id", "created_at", "updated_at", "is_active", })
