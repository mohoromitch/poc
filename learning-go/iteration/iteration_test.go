package iteration

import (
	"fmt"
	"testing"
)

func TestRepeat(t *testing.T) {
	assertRepeatedIsExpected := func(t testing.TB, repeated, expected string) {
		t.Helper()
		if repeated != expected {
			t.Errorf("expected %q but got %q", expected, repeated)
		}
	}
	t.Run("repeats the given character 5 times", func(t *testing.T) {
		repeated := Repeat("a", 5)
		expected := "aaaaa"
		assertRepeatedIsExpected(t, repeated, expected)
	})
	t.Run("repeats the given character once", func(t *testing.T) {
		repeated := Repeat("a", 1)
		expected := "a"
		assertRepeatedIsExpected(t, repeated, expected)
	})
	t.Run("repeats the given character zero times", func(t *testing.T) {
		repeated := Repeat("a", 0)
		expected := ""
		assertRepeatedIsExpected(t, repeated, expected)
	})
}

func ExampleRepeat() {
	repeated := Repeat("a", 5)
	fmt.Println(repeated)
	// Output: aaaaa
}

func BenchmarkRepeat(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Repeat("a", 5)
	}
}
