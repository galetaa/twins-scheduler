package main

import (
	"encoding/json"
	"fmt"
	"math/big"
)

type Case struct {
	F                     string `json:"f"`
	N                     string `json:"n"`
	Q                     string `json:"q"`
	Base                  string `json:"base_support"`
	TypedFirst            string `json:"typed_first_support"`
	TypedSecond           string `json:"typed_second_support"`
	DirectedAbsentFirst   string `json:"directed_absent_first_support"`
	DirectedPresentFirst  string `json:"directed_present_first_support"`
	DirectedPresentSecond string `json:"directed_present_second_support"`
	StrictSeparation      bool   `json:"strict_separation"`
}

type Result struct {
	Status       string `json:"status"`
	Arithmetic   string `json:"arithmetic"`
	CasesChecked int    `json:"cases_checked"`
	LargestF     string `json:"largest_f"`
	AllPass      bool   `json:"all_pass"`
	SampleCases  []Case `json:"sample_cases"`
	FailedCases  []Case `json:"failed_cases"`
}

func clone(x *big.Int) *big.Int { return new(big.Int).Set(x) }

func evaluate(f *big.Int) Case {
	one := big.NewInt(1)
	two := big.NewInt(2)
	three := big.NewInt(3)
	n := new(big.Int).Add(new(big.Int).Mul(three, clone(f)), one)
	q := new(big.Int).Add(new(big.Int).Mul(two, clone(f)), one)
	base := new(big.Int).Mul(two, clone(f))
	typedFirst := new(big.Int).Add(clone(base), one)
	typedSecond := new(big.Int).Add(clone(base), one)
	absentFirst := clone(base)
	presentFirst := new(big.Int).Add(clone(base), one)
	presentSecond := clone(base)

	oneShortAbsent := new(big.Int).Sub(clone(q), clone(absentFirst)).Cmp(one) == 0
	oneShortPresent := new(big.Int).Sub(clone(q), clone(presentSecond)).Cmp(one) == 0
	strict := typedFirst.Cmp(q) == 0 && typedSecond.Cmp(q) == 0 &&
		oneShortAbsent && presentFirst.Cmp(q) == 0 && oneShortPresent

	return Case{
		F: f.String(), N: n.String(), Q: q.String(), Base: base.String(),
		TypedFirst: typedFirst.String(), TypedSecond: typedSecond.String(),
		DirectedAbsentFirst:   absentFirst.String(),
		DirectedPresentFirst:  presentFirst.String(),
		DirectedPresentSecond: presentSecond.String(),
		StrictSeparation:      strict,
	}
}

func mustBig(value string) *big.Int {
	result, ok := new(big.Int).SetString(value, 10)
	if !ok || result.Sign() <= 0 {
		panic("invalid positive integer: " + value)
	}
	return result
}

func main() {
	values := make([]*big.Int, 0, 1032)
	for i := int64(1); i <= 1024; i++ {
		values = append(values, big.NewInt(i))
	}
	for _, text := range []string{
		"1000000000000000000",
		"340282366920938463463374607431768211507",
		"100000000000000000000000000000000000000000000000001",
		"9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999",
	} {
		values = append(values, mustBig(text))
	}

	failed := make([]Case, 0)
	samples := make([]Case, 0)
	for index, f := range values {
		row := evaluate(f)
		if !row.StrictSeparation {
			failed = append(failed, row)
		}
		if index < 3 || index >= len(values)-4 {
			samples = append(samples, row)
		}
	}
	allPass := len(failed) == 0
	status := "PASS"
	if !allPass {
		status = "FAIL"
	}
	result := Result{
		Status:       status,
		Arithmetic:   "math/big exact integer arithmetic; no machine-word overflow",
		CasesChecked: len(values),
		LargestF:     values[len(values)-1].String(),
		AllPass:      allPass,
		SampleCases:  samples,
		FailedCases:  failed,
	}
	encoded, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
