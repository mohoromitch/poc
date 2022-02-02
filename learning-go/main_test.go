package main

import "testing"

func TestHello(t *testing.T) {
	assertCorrectMessage := func(t testing.TB, got, want string) {
		t.Helper()
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	}
	t.Run("say 'Hello, World', when the empty string is supplied.", func(t *testing.T) {
		got := Hello("")
		want := "Hello, World"
		assertCorrectMessage(t, got, want)
	})
	t.Run("say hello to a person", func(t *testing.T) {
		got := Hello("Mitchell")
		want := "Hello, Mitchell"
		assertCorrectMessage(t, got, want)
	})
}
