package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

// RelationshipsFollowing represents the outermost structure
type RelationshipsFollowing struct {
	RelationshipsFollowing []Relationship `json:"relationships_following"`
}

// Relationship represents each relationship entry in the JSON
type Relationship struct {
	Title string `json:"title"`
	// MediaListData  []string     `json:"media_list_data"`
	StringListData []StringData `json:"string_list_data"`
}

// StringData represents each string data entry in the relationship
type StringData struct {
	Href      string `json:"href"`
	Value     string `json:"value"`
	Timestamp int    `json:"timestamp"`
}

type Profile struct {
	Username string
	Link     string
}

// Usage of the helper function in the main function
func main() {
	following, err := GetFollowingFromFile("./following.json")
	if err != nil {
		log.Fatalf("Failed to parse following list: %v", err)
	}
	followers, err := GetFollowersFromFile("./followers_1.json")
	if err != nil {
		log.Fatalf("Failed to parse followers list: %v", err)
	}

	log.Println(following)
	log.Printf("total following: %d\n", len(following))

	log.Println(followers)
	log.Printf("total followers: %d\n", len(followers))

	followersMap := make(map[string]bool)

	// Fill followersMap
	for _, profile := range followers {
		followersMap[profile.Username] = true
	}

	// Check each following and add to the map if not in followersMap
	newProfiles := []*Profile{}
	for _, profile := range following {
		if !followersMap[profile.Username] {
			newProfiles = append(newProfiles, profile)
		}
	}

	// Log the new profiles
	log.Println("New profiles that are in following but not in followers:")
	for _, profile := range newProfiles {
		log.Printf("Username: %s, Link: %s\n", profile.Username, profile.Link)
	}
}

func GetFollowingFromFile(filename string) ([]*Profile, error) {
	var relationships RelationshipsFollowing
	var profiles []*Profile

	// Read the JSON file
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %v", err)
	}

	err = json.Unmarshal(data, &relationships)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal JSON data: %v", err)
	}

	profiles = make([]*Profile, len(relationships.RelationshipsFollowing))
	for i, val := range relationships.RelationshipsFollowing {
		profiles[i] = &Profile{
			Username: val.StringListData[0].Value,
			Link:     val.StringListData[0].Href,
		}
	}

	return profiles, nil
}

func GetFollowersFromFile(filename string) ([]*Profile, error) {
	var followers []Relationship
	var profiles []*Profile

	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %v", err)
	}

	err = json.Unmarshal(data, &followers)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal JSON data: %v", err)
	}

	profiles = make([]*Profile, len(followers))
	for i, val := range followers {
		profiles[i] = &Profile{
			Username: val.StringListData[0].Value,
			Link:     val.StringListData[0].Href,
		}
	}

	return profiles, nil
}
