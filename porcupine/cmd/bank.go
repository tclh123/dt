package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	p "porcupine"
)

const (
	bank_account_num = 5
	init_balance     = 10000
)

var (
	record_filepath = flag.String("f", "", "the record file")
)

type Bank struct {
}

type BankState []uint64

func (s BankState) Equal(balances BankState) bool {
	if len(s) != len(balances) {
		return false
	}
	for i, balance := range balances {
		if s[i] != balance {
			return false
		}
	}
	return true
}

type BankInput struct {
	Op           uint8  `json:"op"`
	From_account uint8  `json:"from_account"`
	To_account   uint8  `json:"to_account"`
	Amount       uint64 `json:"amount"`
}

type BankOutput struct {
	Balances BankState `json:"balances"`
	Ok       bool      `json:"ok"`
	Unknown  bool      `json:"unknown"`
}

type BankOperation struct {
	Input      BankInput  `json:"input"`
	Output     BankOutput `json:"output"`
	CallTime   int64      `json:"call_time"`
	ReturnTime int64      `json:"return_time"`
}

// Initial state of the system.
func (*Bank) Init() interface{} {
	balances := make([]uint64, bank_account_num)
	for i := 0; i < bank_account_num; i++ {
		balances[i] = init_balance
	}
	return BankState(balances)
}

// Step function for the system. Returns whether or not the system
// could take this step with the given inputs and outputs and also
// returns the new state. This should not mutate the existing state.
func (*Bank) Step(state, input, output interface{}) (bool, interface{}) {
	inp := input.(BankInput)
	out := output.(BankOutput)
	st := state.(BankState)

	// read
	if inp.Op == 0 {
		ok := (out.Ok && st.Equal(out.Balances)) || out.Unknown
		return ok, st
	}

	// write
	ok := (st[inp.From_account] >= inp.Amount && out.Ok) || (st[inp.From_account] < inp.Amount && !out.Ok) || out.Unknown

	newBalances := append([]uint64(nil), st...)
	if newBalances[inp.From_account] >= inp.Amount {
		newBalances[inp.From_account] -= inp.Amount
		newBalances[inp.To_account] += inp.Amount
	}

	return ok, BankState(newBalances)
}

func (*Bank) Equal(state1, state2 interface{}) bool {
	return state1.(BankState).Equal(state2.(BankState))
}

func ReadOperations(filepath *string) []p.Operation {
	content, err := ioutil.ReadFile(*filepath)
	if err != nil {
		log.Fatal(err)
	}

	var ops []BankOperation
	err = json.Unmarshal(content, &ops)
	if err != nil {
		log.Fatal(err)
	}

	// fmt.Println("Bank Operations:", ops)

	ops2 := make([]p.Operation, len(ops))
	for i, op := range ops {
		ops2[i] = p.Operation{
			Input:  op.Input,
			Call:   int64(op.CallTime),
			Output: op.Output,
			Return: int64(op.ReturnTime),
		}
	}
	// fmt.Println("P Operations:", ops2)

	return ops2
}

func main() {
	flag.Parse()
	fmt.Println("test bank")

	// ops := []p.Operation{
	// 	{BankInput{op: 0}, 0, BankOutput{balances: []uint64{10000, 10000, 10000, 10000, 10000}, ok: true}, 10},
	// 	{BankInput{1, 0, 1, 1000}, 25, BankOutput{ok: true}, 75},
	// 	{BankInput{op: 0}, 30, BankOutput{balances: []uint64{9000, 11000, 10000, 10000, 10000}, ok: true}, 60},
	// }

	ops := ReadOperations(record_filepath)

	b := Bank{}
	res := p.CheckOperations(p.Model{Init: b.Init, Step: b.Step, Equal: b.Equal}, ops)
	fmt.Println("result is", res)
	if !res {
		os.Exit(1)
	}
	os.Exit(0)
}
