package main

import "testing"

func TestHello(t *testing.T) {
	got := Hello("Mitchell")
	want := "Hello, Mitchell!"

	if got != want {
		t.Errorf("got %q want %q", got, want)
	}
}
