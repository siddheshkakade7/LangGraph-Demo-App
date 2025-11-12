from app.graph import compile_graph

def test_add_numbers_route():
    g = compile_graph()
    out = g.invoke({"user_input": "Please add 2 + 3"})
    assert out["response"] == "Sum is 5.0"

def test_uppercase_route():
    g = compile_graph()
    out = g.invoke({"user_input": "uppercase hello world"})
    assert out["response"] == "Uppercased: UPPERCASE HELLO WORLD"

def test_default_route():
    g = compile_graph()
    out = g.invoke({"user_input": "hello"})
    assert "I received:" in out["response"]
