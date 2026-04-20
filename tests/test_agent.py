from agentforge_echo.agents.echo_agent import EchoRunner


def test_runner_reverses():
    assert EchoRunner().run("hello") == "olleh"


def test_runner_empty_string():
    assert EchoRunner().run("") == ""


def test_runner_is_deterministic():
    r = EchoRunner()
    assert r.run("agentforge") == r.run("agentforge") == "egroftnega"
