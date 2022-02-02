package main

import "fmt"

const englishHelloPrefix = "Hello, "

func Hello(name string) string {
	if name == "" {
		return englishHelloPrefix + "World"
	} else {
		return englishHelloPrefix + name
	}
}

func main() {
	fmt.Println(Hello("world"))
}
