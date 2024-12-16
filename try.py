from __future__ import annotations

from pydantic import BaseModel


class A(BaseModel):
    a: A = None


a = A()
a.a = a
a2 = A()
a2.a = a2

print(a == a2)
