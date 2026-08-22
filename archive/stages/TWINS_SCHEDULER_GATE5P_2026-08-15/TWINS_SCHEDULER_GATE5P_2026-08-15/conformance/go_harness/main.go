// Command harness_fixture is a dependency-free executable extraction of the
// message-admission and pending-queue semantics in relab/hotstuff twins/network.go
// at commit 3179c6e62929294961acbfd9bf8445769716a121.
//
// It intentionally does not execute consensus code. Its sole purpose is to make
// the pinned network semantics executable and differentially comparable with the
// Python abstraction used by Gate 4'.
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "sort"
)

type View struct {
    Partitions [][]string `json:"partitions"`
}

type Message struct {
    ID       string `json:"id"`
    Sender   string `json:"sender"`
    Receiver string `json:"receiver"`
    Type     string `json:"type"`
    View     int    `json:"view"`
}

type Case struct {
    ID         string    `json:"id"`
    Views      []View    `json:"views"`
    DropTypes  []string  `json:"drop_types"`
    GlobalView int       `json:"global_view"`
    Messages   []Message `json:"messages"`
    Ticks      int       `json:"ticks"`
}

type Input struct {
    Cases []Case `json:"cases"`
}

type CaseResult struct {
    ID              string     `json:"id"`
    DroppedIDs      []string   `json:"dropped_ids"`
    DeliveredByTick [][]string `json:"delivered_by_tick"`
    PendingIDs      []string   `json:"pending_ids"`
    FinalGlobalView int        `json:"final_global_view"`
}

type Output struct {
    Results []CaseResult `json:"results"`
}

func contains(items []string, target string) bool {
    for _, item := range items {
        if item == target {
            return true
        }
    }
    return false
}

// shouldDrop mirrors Network.shouldDrop in the pinned source snapshot:
//   * view <= 0: do not drop;
//   * view beyond the configured scenario: drop every message;
//   * same partition: do not drop;
//   * otherwise drop only configured message types.
func shouldDrop(c Case, m Message) bool {
    i := m.View - 1
    if i < 0 {
        return false
    }
    if i >= len(c.Views) {
        return true
    }
    for _, partition := range c.Views[i].Partitions {
        if contains(partition, m.Sender) && contains(partition, m.Receiver) {
            return false
        }
    }
    return contains(c.DropTypes, m.Type)
}

func execute(c Case) CaseResult {
    globalView := c.GlobalView
    pending := make([]Message, 0, len(c.Messages))
    dropped := make([]string, 0)

    // This is the sendMessage admission point: the message keeps the sender's
    // effective view and is queued iff shouldDrop returns false.
    for _, m := range c.Messages {
        if shouldDrop(c, m) {
            dropped = append(dropped, m.ID)
        } else {
            pending = append(pending, m)
        }
    }

    deliveredByTick := make([][]string, 0, c.Ticks)
    for tick := 0; tick < c.Ticks; tick++ {
        next := make([]Message, 0, len(pending))
        delivered := make([]string, 0)
        for _, m := range pending {
            if m.View > globalView {
                next = append(next, m)
                continue
            }
            delivered = append(delivered, m.ID)
        }
        if len(pending) == len(next) {
            globalView++
        }
        pending = next
        deliveredByTick = append(deliveredByTick, delivered)
    }

    pendingIDs := make([]string, 0, len(pending))
    for _, m := range pending {
        pendingIDs = append(pendingIDs, m.ID)
    }
    // Input order is deterministic; explicit sorting makes the output robust if
    // a future fixture changes the storage representation.
    sort.Strings(dropped)
    sort.Strings(pendingIDs)

    return CaseResult{
        ID:              c.ID,
        DroppedIDs:      dropped,
        DeliveredByTick: deliveredByTick,
        PendingIDs:      pendingIDs,
        FinalGlobalView: globalView,
    }
}

func main() {
    decoder := json.NewDecoder(os.Stdin)
    decoder.DisallowUnknownFields()
    var input Input
    if err := decoder.Decode(&input); err != nil {
        fmt.Fprintf(os.Stderr, "decode input: %v\n", err)
        os.Exit(2)
    }

    output := Output{Results: make([]CaseResult, 0, len(input.Cases))}
    for _, c := range input.Cases {
        if c.GlobalView < 0 || c.Ticks < 0 {
            fmt.Fprintf(os.Stderr, "invalid case %q\n", c.ID)
            os.Exit(2)
        }
        output.Results = append(output.Results, execute(c))
    }

    encoder := json.NewEncoder(os.Stdout)
    encoder.SetEscapeHTML(false)
    encoder.SetIndent("", "  ")
    if err := encoder.Encode(output); err != nil {
        fmt.Fprintf(os.Stderr, "encode output: %v\n", err)
        os.Exit(2)
    }
}
