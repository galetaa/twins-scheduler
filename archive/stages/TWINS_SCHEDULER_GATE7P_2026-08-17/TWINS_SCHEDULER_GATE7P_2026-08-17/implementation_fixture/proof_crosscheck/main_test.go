package main

import (
	"math/big"
	"testing"
)

func TestSmallAndHugeParameters(t *testing.T) {
	for _, text := range []string{"1", "2", "1024", "100000000000000000000000000000000000001"} {
		row := evaluate(mustBig(text))
		if !row.StrictSeparation {
			t.Fatalf("T3 arithmetic failed for f=%s: %+v", text, row)
		}
	}
}

func TestQuorumGapIsExactlyOne(t *testing.T) {
	f := big.NewInt(17)
	row := evaluate(f)
	q := mustBig(row.Q)
	base := mustBig(row.Base)
	if new(big.Int).Sub(q, base).Cmp(big.NewInt(1)) != 0 {
		t.Fatalf("q-base is not one: q=%s base=%s", q, base)
	}
}
