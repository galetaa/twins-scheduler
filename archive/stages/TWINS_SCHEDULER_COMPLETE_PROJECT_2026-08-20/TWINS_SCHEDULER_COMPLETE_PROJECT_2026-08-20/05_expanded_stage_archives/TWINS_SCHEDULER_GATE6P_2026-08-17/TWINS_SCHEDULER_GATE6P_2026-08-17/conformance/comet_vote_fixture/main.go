// comet_vote_fixture is a dependency-free executable abstraction of the
// duplicate-vote decision in CometBFT v0.40.0 types/vote_set.go.
//
// unique=true models AddVote/getVote: an identical logical vote is ignored.
// unique=false is the controlled local mutation used by Gate 5': message
// instances, not validator identities, contribute to quorum.
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
)

type Request struct {
	Unique bool     `json:"unique"`
	Quorum int      `json:"quorum"`
	Votes  []string `json:"votes"`
}

type Response struct {
	Contributions int      `json:"contributions"`
	Quorum        bool     `json:"quorum"`
	Accepted      []string `json:"accepted"`
}

func process(req Request) Response {
	seen := make(map[string]bool)
	accepted := make([]string, 0, len(req.Votes))
	for _, validator := range req.Votes {
		if req.Unique && seen[validator] {
			continue
		}
		seen[validator] = true
		accepted = append(accepted, validator)
	}
	return Response{
		Contributions: len(accepted),
		Quorum:        len(accepted) >= req.Quorum,
		Accepted:      accepted,
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	encoder := json.NewEncoder(os.Stdout)
	for scanner.Scan() {
		var req Request
		if err := json.Unmarshal(scanner.Bytes(), &req); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
		if req.Quorum <= 0 {
			fmt.Fprintln(os.Stderr, "quorum must be positive")
			os.Exit(2)
		}
		if err := encoder.Encode(process(req)); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(2)
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
}
